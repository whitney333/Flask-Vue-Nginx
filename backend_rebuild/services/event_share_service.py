"""Unguessable, revocable share links that expose a read-only offline event report."""
import re
import secrets
from datetime import datetime
from typing import Any, Optional

from bson import ObjectId
from bson.errors import InvalidId
from mongoengine.errors import DoesNotExist

from models.event_model import OfflineEvent, OfflineSalesSnapshot

# 32 random bytes -> 43 url-safe base64 characters (256 bits of entropy).
TOKEN_BYTES = 32
TOKEN_PATTERN = re.compile(r"^[A-Za-z0-9_-]{43}$")

PUBLIC_EVENT_FIELDS = (
    "event_name",
    "type",
    "session",
    "held_country",
    "held_city",
    "venue",
    "organizer",
)
PUBLIC_EVENT_DATE_FIELDS = ("event_date", "ticket_release", "ticket_close")
PUBLIC_TICKET_ITEM_FIELDS = (
    "name",
    "type",
    "currency",
    "price",
    "total_quantity",
    "sold",
    "refund",
    "net_sold",
    "revenue",
    "sell_through_rate",
)


def _isoformat(value: Optional[datetime]) -> Optional[str]:
    return value.isoformat() if value else None


def _find_event(event_id: str) -> Optional[OfflineEvent]:
    try:
        object_id = ObjectId(str(event_id))
    except (InvalidId, TypeError):
        return None
    return OfflineEvent.objects(id=object_id).first()


class EventShareService:
    @staticmethod
    def generate_token() -> str:
        return secrets.token_urlsafe(TOKEN_BYTES)

    @staticmethod
    def is_valid_token_format(token: Any) -> bool:
        return isinstance(token, str) and bool(TOKEN_PATTERN.fullmatch(token))

    @classmethod
    def create_share_link(cls, event_id: str) -> Optional[dict]:
        """Create (or rotate) the event's share link. Any previous link stops working."""
        event = _find_event(event_id)
        if not event:
            return None

        token = cls.generate_token()
        now = datetime.utcnow()
        # MongoDB keeps milliseconds; trim now so this response matches later reads exactly
        created_at = now.replace(microsecond=now.microsecond // 1000 * 1000)
        event.update(
            set__share_token=token,
            set__share_token_created_at=created_at,
        )

        return {
            "share_token": token,
            "share_token_created_at": created_at.isoformat(),
        }

    @staticmethod
    def get_share_link(event_id: str) -> Optional[dict]:
        """The event's active link (both fields None when there is none), or None if no event."""
        event = _find_event(event_id)
        if not event:
            return None

        return {
            "share_token": event.share_token or None,
            "share_token_created_at": _isoformat(event.share_token_created_at),
        }

    @staticmethod
    def revoke_share_link(event_id: str) -> bool:
        event = _find_event(event_id)
        if not event:
            return False

        event.update(unset__share_token=True, unset__share_token_created_at=True)
        return True

    @classmethod
    def get_public_report(cls, token: Any) -> Optional[dict]:
        # Validate before querying: blocks operator injection and skips pointless lookups.
        if not cls.is_valid_token_format(token):
            return None

        event = OfflineEvent.objects(share_token=token).first()
        if not event:
            return None

        snapshots = OfflineSalesSnapshot.objects(event_id=str(event.id)).order_by("-observed_at")

        return {
            "event": cls._serialize_event(event),
            "artists": [cls._serialize_artist(item) for item in (event.artists or [])],
            "snapshots": [cls._serialize_snapshot(s) for s in snapshots],
        }

    # Public serializers: allowlists only, so new model fields stay private by default.
    @staticmethod
    def _serialize_event(event: OfflineEvent) -> dict:
        text_fields = {field: getattr(event, field, None) for field in PUBLIC_EVENT_FIELDS}
        date_fields = {
            field: _isoformat(getattr(event, field, None)) for field in PUBLIC_EVENT_DATE_FIELDS
        }
        return {**text_fields, **date_fields}

    @staticmethod
    def _serialize_artist(item) -> dict:
        en_name = item.artist_en_name or ""
        kr_name = item.artist_kr_name or ""
        image_url = None
        try:
            artist = item.artist_id.fetch() if item.artist_id else None
        except (DoesNotExist, AttributeError):
            artist = None

        if artist:
            en_name = artist.english_name or en_name
            kr_name = artist.korean_name or kr_name
            image_url = getattr(artist, "image_url", None)

        return {
            "artist_en_name": en_name,
            "artist_kr_name": kr_name,
            "image_url": image_url,
        }

    @staticmethod
    def _serialize_snapshot(snapshot: OfflineSalesSnapshot) -> dict:
        gender = getattr(snapshot, "gender_distribution", None)
        age = getattr(snapshot, "age_distribution", None)
        return {
            "id": str(snapshot.id),
            "snapshot_name": snapshot.snapshot_name,
            "snapshot_type": getattr(snapshot, "snapshot_type", None),
            "observed_at": _isoformat(snapshot.observed_at),
            "ticket_items": [
                {field: getattr(item, field, None) for field in PUBLIC_TICKET_ITEM_FIELDS}
                for item in (snapshot.ticket_items or [])
            ],
            "gender_distribution": gender.to_mongo().to_dict() if gender else None,
            "age_distribution": age.to_mongo().to_dict() if age else None,
        }
