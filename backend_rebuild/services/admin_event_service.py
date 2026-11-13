from datetime import datetime
from bson import ObjectId
from mongoengine.errors import DoesNotExist, ValidationError
from models.artist_model import Artists
from models.event_model import (
    OfflineEvent,
    OfflineSalesSnapshot,
    TicketBenefitItem,
    EventArtist,
    GenderDistribution,
    AgeDistribution,
)


class OfflineEventService:
    @staticmethod
    def _parse_datetime(value, field_name, required=False):
        if value in (None, ""):
            if required:
                raise ValueError(f"{field_name} is required")
            return None

        if isinstance(value, datetime):
            return value

        if isinstance(value, str):
            normalized = value.strip()
            if normalized.endswith("Z"):
                normalized = normalized[:-1] + "+00:00"
            try:
                return datetime.fromisoformat(normalized)
            except ValueError:
                try:
                    return datetime.strptime(normalized, "%Y-%m-%d")
                except ValueError:
                    raise ValueError(f"{field_name} must be an ISO date or datetime")

        raise ValueError(f"{field_name} must be an ISO date or datetime")

    @staticmethod
    def _clean_string(value):
        if value in (None, "", "null"):
            return None
        return str(value).strip()

    @classmethod
    def _resolve_artists(cls, data):
        """
        支援接收 artist_ids (陣列) 或是向下相容舊版的單一 artist_id
        回傳 EventArtist 嵌入式文件的列表
        """
        artist_ids = data.get("artist_ids")
        if not artist_ids and data.get("artist_id"):
            artist_ids = [data.get("artist_id")]

        if not artist_ids or not isinstance(artist_ids, list):
            return []

        resolved_event_artists = []
        for aid in artist_ids:
            try:
                artist = Artists.objects(id=ObjectId(str(aid))).first()
            except Exception:
                artist = None

            if artist:
                resolved_event_artists.append(
                    EventArtist(
                        artist_id=artist,
                        artist_en_name=artist.english_name or "",
                        artist_kr_name=artist.korean_name or ""
                    )
                )

        return resolved_event_artists

    @staticmethod
    def serialize_event(event):
        artists_data = []
        if event.artists:
            for item in event.artists:
                # 嘗試即時 fetch 取得最新名稱，若失敗則使用內嵌快照名稱
                en_name = item.artist_en_name
                kr_name = item.artist_kr_name
                a_id = None
                try:
                    if item.artist_id:
                        fetched = item.artist_id.fetch()
                        if fetched:
                            en_name = fetched.english_name or en_name
                            kr_name = fetched.korean_name or kr_name
                            a_id = str(fetched.id)
                except (DoesNotExist, AttributeError):
                    pass

                if not a_id and item.artist_id:
                    a_id = str(item.artist_id.pk)

                artists_data.append({
                    "id": a_id,
                    "artist_id": a_id,
                    "artist_en_name": en_name,
                    "artist_kr_name": kr_name
                })

        # 為了向下相容前端單選欄位，取第一個藝人作為代表
        primary_artist = artists_data[0] if artists_data else {}

        return {
            "id": str(event.id),
            "event_id": str(event.id),
            "event_name": event.event_name,
            "type": event.type,
            "artist_ids": [a["artist_id"] for a in artists_data if a["artist_id"]],
            "artist_id": primary_artist.get("artist_id"),
            "artist_en_name": primary_artist.get("artist_en_name", ""),
            "artist_kr_name": primary_artist.get("artist_kr_name", ""),
            "artist_name": primary_artist.get("artist_en_name", ""),
            "artists": artists_data,
            "event_date": event.event_date.isoformat() if event.event_date else None,
            "session": event.session,
            "held_country": event.held_country,
            "held_city": event.held_city,
            "venue": event.venue,
            "organizer": event.organizer,
            "ticket_release": event.ticket_release.isoformat() if event.ticket_release else None,
            "ticket_close": event.ticket_close.isoformat() if event.ticket_close else None,
            # share-link status only: admins fetch the link itself from GET /events/<id>/share,
            # which keeps the token out of list payloads and anything that logs them
            "has_share_link": bool(getattr(event, "share_token", None)),
            "share_token_created_at": (
                event.share_token_created_at.isoformat()
                if getattr(event, "share_token_created_at", None) else None
            ),
            "created_at": event.created_at.isoformat() if event.created_at else None,
            "updated_at": event.updated_at.isoformat() if event.updated_at else None
        }

    # Event CRUD
    @staticmethod
    def create_event(data, current_user):
        required_fields = [
            "event_name",
            "type",
            "event_date",
            "session",
            "held_country",
            "held_city",
            "venue",
            "organizer",
            "ticket_release",
            "ticket_close"
        ]
        for field in required_fields:
            if data.get(field) in (None, ""):
                raise ValueError(f"{field} is required")

        artists_list = OfflineEventService._resolve_artists(data)

        event = OfflineEvent(
            event_name=OfflineEventService._clean_string(data.get("event_name")),
            type=OfflineEventService._clean_string(data.get("type")),
            artists=artists_list,
            event_date=OfflineEventService._parse_datetime(data.get("event_date"), "event_date", required=True),
            session=OfflineEventService._clean_string(data.get("session")),
            held_country=OfflineEventService._clean_string(data.get("held_country")),
            held_city=OfflineEventService._clean_string(data.get("held_city")),
            venue=OfflineEventService._clean_string(data.get("venue")),
            organizer=OfflineEventService._clean_string(data.get("organizer")),
            ticket_release=OfflineEventService._parse_datetime(data.get("ticket_release"), "ticket_release", required=True),
            ticket_close=OfflineEventService._parse_datetime(data.get("ticket_close"), "ticket_close", required=True),
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        event.save()

        return OfflineEventService.serialize_event(event)

    @staticmethod
    def get_events(page=1, limit=20, search=None):
        page = max(int(page), 1)
        limit = max(min(int(limit), 100), 1)

        query = {}
        if search:
            query["__raw__"] = {
                "$or": [
                    {"event_name": {"$regex": search, "$options": "i"}},
                    {"artists.artist_en_name": {"$regex": search, "$options": "i"}},
                    {"artists.artist_kr_name": {"$regex": search, "$options": "i"}},
                    {"held_country": {"$regex": search, "$options": "i"}},
                    {"held_city": {"$regex": search, "$options": "i"}},
                    {"venue": {"$regex": search, "$options": "i"}},
                    {"organizer": {"$regex": search, "$options": "i"}}
                ]
            }

        events_query = OfflineEvent.objects(**query).order_by("-event_date")
        total = events_query.count()
        events = list(events_query.skip((page - 1) * limit).limit(limit))

        return {
            "total": total,
            "page": page,
            "limit": limit,
            "count": len(events),
            "data": [OfflineEventService.serialize_event(event) for event in events]
        }

    @staticmethod
    def get_event(event_id):
        event = OfflineEvent.objects(id=event_id).first()
        if not event:
            return None

        return OfflineEventService.serialize_event(event)

    @staticmethod
    def update_event(event_id, data, current_user):
        event = OfflineEvent.objects(id=event_id).first()
        if not event:
            return None

        text_fields = [
            "event_name",
            "type",
            "session",
            "held_country",
            "held_city",
            "venue",
            "organizer"
        ]
        for field in text_fields:
            if field in data:
                setattr(event, field, OfflineEventService._clean_string(data.get(field)))

        for field in ["event_date", "ticket_release", "ticket_close"]:
            if field in data:
                setattr(event, field, OfflineEventService._parse_datetime(data.get(field), field, required=True))

        if "artist_ids" in data or "artist_id" in data:
            event.artists = OfflineEventService._resolve_artists(data)

        event.updated_at = datetime.utcnow()
        try:
            event.save()
        except ValidationError as exc:
            raise ValueError(str(exc))

        return OfflineEventService.serialize_event(event)

    @staticmethod
    def delete_event(event_id):
        event = OfflineEvent.objects(id=event_id).first()
        if not event:
            return False

        event.delete()
        return True

    # Snapshot CRUD
    @staticmethod
    def _get_user_id(current_user):
        if not current_user:
            return None
        if isinstance(current_user, dict):
            return str(current_user.get("_id") or current_user.get("id") or "")
        if hasattr(current_user, "id"):
            return str(current_user.id)
        return str(current_user)

    # Audience demographics are only allowed on the Closed snapshot.
    CLOSED_SNAPSHOT_NAMES = {"closed"}

    @classmethod
    def _is_closed_snapshot(cls, snapshot_name, snapshot_type=None):
        if snapshot_type:
            return str(snapshot_type).strip().lower() == "closed"
        return (snapshot_name or "").strip().lower() in cls.CLOSED_SNAPSHOT_NAMES

    @staticmethod
    def _parse_distribution(data, fields, field_name):
        if not isinstance(data, dict):
            raise ValueError(f"{field_name} must be an object")

        result = {}
        for field in fields:
            value = data.get(field, 0)
            if isinstance(value, bool):
                raise ValueError(f"{field_name}.{field} must be a number")
            try:
                value = float(value)
            except (TypeError, ValueError):
                raise ValueError(f"{field_name}.{field} must be a number")

            if not 0 <= value <= 100:
                raise ValueError(f"{field_name}.{field} must be between 0 and 100")
            result[field] = value

        if round(sum(result.values()), 2) != 100:
            raise ValueError(f"{field_name} percentages must total 100")

        return result

    @classmethod
    def _build_demographics(cls, data, snapshot_name, snapshot_type=None):
        has_gender = data.get("gender_distribution") not in (None, {})
        has_age = data.get("age_distribution") not in (None, {})

        is_closed = cls._is_closed_snapshot(snapshot_name, snapshot_type)

        if not is_closed:
            if has_gender or has_age:
                raise ValueError(
                    "Gender and age distributions can only be saved on the Closed snapshot"
                )
            return None, None

        if not has_gender and not has_age:
            return None, None

        # If demographics are submitted for the Closed snapshot, both
        # distributions must be complete and each must total 100%.
        if not has_gender or not has_age:
            raise ValueError(
                "Both gender_distribution and age_distribution are required when saving demographics"
            )

        gender = cls._parse_distribution(
            data["gender_distribution"],
            ["male", "female", "unknown"],
            "gender_distribution",
        )
        age = cls._parse_distribution(
            data["age_distribution"],
            ["age_10s", "age_20s", "age_30s", "age_40s", "age_50_plus"],
            "age_distribution",
        )

        return GenderDistribution(**gender), AgeDistribution(**age)

    @staticmethod
    def serialize_snapshot(snapshot):
        ticket_items_data = []
        if snapshot.ticket_items:
            for item in snapshot.ticket_items:
                ticket_items_data.append({
                    "name": item.name,
                    "type": item.type,
                    "currency": item.currency,
                    "price": item.price,
                    "total_quantity": item.total_quantity,
                    "sold": item.sold,
                    "refund": item.refund,
                    "net_sold": item.net_sold,
                    "revenue": item.revenue,
                    "sell_through_rate": item.sell_through_rate
                })

        return {
            "id": str(snapshot.id),
            "snapshot_name": snapshot.snapshot_name,
            "observed_at": snapshot.observed_at.isoformat() if snapshot.observed_at else None,
            "event_id": snapshot.event_id,
            "ticket_items": ticket_items_data,
            "snapshot_type": getattr(snapshot, "snapshot_type", None),
            "gender_distribution": (
                snapshot.gender_distribution.to_mongo().to_dict()
                if getattr(snapshot, "gender_distribution", None) else None
            ),
            "age_distribution": (
                snapshot.age_distribution.to_mongo().to_dict()
                if getattr(snapshot, "age_distribution", None) else None
            ),
            "created_by": snapshot.created_by,
            "updated_by": snapshot.updated_by,
            "created_at": snapshot.created_at.isoformat() if snapshot.created_at else None,
            "updated_at": snapshot.updated_at.isoformat() if snapshot.updated_at else None
        }

    @staticmethod
    def get_snapshots(event_id):
        snapshots = OfflineSalesSnapshot.objects(event_id=str(event_id)).order_by("-observed_at")
        return [OfflineEventService.serialize_snapshot(s) for s in snapshots]

    @staticmethod
    def create_snapshot(event_id, data, current_user):
        event = OfflineEvent.objects(id=event_id).first()
        if not event:
            raise ValueError("Event not found")

        snapshot_name = OfflineEventService._clean_string(data.get("snapshot_name"))
        snapshot_type = OfflineEventService._clean_string(data.get("snapshot_type"))
        observed_at = OfflineEventService._parse_datetime(
            data.get("observed_at"), "observed_at", required=True
        )
        raw_items = data.get("ticket_items", [])

        if not snapshot_name:
            raise ValueError("snapshot_name is required")
        if not isinstance(raw_items, list):
            raise ValueError("ticket_items must be a list")

        gender_distribution, age_distribution = (
            OfflineEventService._build_demographics(
                data, snapshot_name, snapshot_type
            )
        )

        ticket_items = []
        for raw in raw_items:
            try:
                price = float(raw.get("price", 0.0))
                total_quantity = int(raw.get("total_quantity", 0))
                sold = int(raw.get("sold", 0))
                refund = int(raw.get("refund", 0))
            except (TypeError, ValueError):
                raise ValueError("Ticket item price and quantities must be numeric")

            if min(price, total_quantity, sold, refund) < 0:
                raise ValueError("Ticket item price and quantities cannot be negative")

            net_sold = max(0, sold - refund)
            revenue = net_sold * price
            sell_through_rate = (
                round((net_sold / total_quantity) * 100, 2)
                if total_quantity > 0 else 0.0
            )

            ticket_items.append(
                TicketBenefitItem(
                    name=OfflineEventService._clean_string(raw.get("name")),
                    type=raw.get("type", "ticket"),
                    currency=raw.get("currency", "TWD"),
                    price=price,
                    total_quantity=total_quantity,
                    sold=sold,
                    refund=refund,
                    net_sold=net_sold,
                    revenue=revenue,
                    sell_through_rate=sell_through_rate,
                )
            )

        user_id = OfflineEventService._get_user_id(current_user)

        snapshot_kwargs = {
            "snapshot_name": snapshot_name,
            "observed_at": observed_at,
            "event_id": str(event_id),
            "ticket_items": ticket_items,
            "gender_distribution": gender_distribution,
            "age_distribution": age_distribution,
            "created_by": user_id,
            "updated_by": user_id,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
        }
        if snapshot_type:
            snapshot_kwargs["snapshot_type"] = snapshot_type

        snapshot = OfflineSalesSnapshot(**snapshot_kwargs)
        try:
            snapshot.save()
        except ValidationError as exc:
            raise ValueError(str(exc))

        return OfflineEventService.serialize_snapshot(snapshot)

    @staticmethod
    def update_snapshot(snapshot_id, data, current_user):
        snapshot = OfflineSalesSnapshot.objects(id=snapshot_id).first()
        if not snapshot:
            return None

        snapshot_name = OfflineEventService._clean_string(
            data.get("snapshot_name", snapshot.snapshot_name)
        )
        snapshot_type = OfflineEventService._clean_string(
            data.get("snapshot_type", getattr(snapshot, "snapshot_type", None))
        )
        if not snapshot_name:
            raise ValueError("snapshot_name is required")

        # Keep current values when demographic keys are omitted. If either key is
        # explicitly included, require both distributions on the Closed snapshot.
        demographic_keys_present = (
                "gender_distribution" in data or "age_distribution" in data
        )
        is_closed = OfflineEventService._is_closed_snapshot(
            snapshot_name, snapshot_type
        )

        if not is_closed:
            if demographic_keys_present and (
                    data.get("gender_distribution") not in (None, {})
                    or data.get("age_distribution") not in (None, {})
            ):
                raise ValueError(
                    "Gender and age distributions can only be saved on the Closed snapshot"
                )
            snapshot.gender_distribution = None
            snapshot.age_distribution = None
        elif demographic_keys_present:
            gender_distribution, age_distribution = (
                OfflineEventService._build_demographics(
                    data, snapshot_name, snapshot_type
                )
            )
            snapshot.gender_distribution = gender_distribution
            snapshot.age_distribution = age_distribution

        if "snapshot_name" in data:
            snapshot.snapshot_name = snapshot_name
        if "snapshot_type" in data and hasattr(snapshot, "snapshot_type"):
            snapshot.snapshot_type = snapshot_type

        if "observed_at" in data:
            snapshot.observed_at = OfflineEventService._parse_datetime(
                data.get("observed_at"), "observed_at", required=True
            )

        if "ticket_items" in data:
            raw_items = data.get("ticket_items")
            if not isinstance(raw_items, list):
                raise ValueError("ticket_items must be a list")

            ticket_items = []
            for raw in raw_items:
                try:
                    price = float(raw.get("price", 0.0))
                    total_quantity = int(raw.get("total_quantity", 0))
                    sold = int(raw.get("sold", 0))
                    refund = int(raw.get("refund", 0))
                except (TypeError, ValueError):
                    raise ValueError("Ticket item price and quantities must be numeric")

                if min(price, total_quantity, sold, refund) < 0:
                    raise ValueError("Ticket item price and quantities cannot be negative")

                net_sold = max(0, sold - refund)
                revenue = net_sold * price
                sell_through_rate = (
                    round((net_sold / total_quantity) * 100, 2)
                    if total_quantity > 0 else 0.0
                )
                ticket_items.append(
                    TicketBenefitItem(
                        name=OfflineEventService._clean_string(raw.get("name")),
                        type=raw.get("type", "ticket"),
                        currency=raw.get("currency", "TWD"),
                        price=price,
                        total_quantity=total_quantity,
                        sold=sold,
                        refund=refund,
                        net_sold=net_sold,
                        revenue=revenue,
                        sell_through_rate=sell_through_rate,
                    )
                )
            snapshot.ticket_items = ticket_items

        snapshot.updated_by = OfflineEventService._get_user_id(current_user)
        snapshot.updated_at = datetime.utcnow()

        try:
            snapshot.save()
        except ValidationError as exc:
            raise ValueError(str(exc))

        return OfflineEventService.serialize_snapshot(snapshot)

    @staticmethod
    def delete_snapshot(snapshot_id):
        snapshot = OfflineSalesSnapshot.objects(id=snapshot_id).first()
        if not snapshot:
            return False
        snapshot.delete()
        return True
