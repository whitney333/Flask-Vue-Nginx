from datetime import datetime

from models.event_model import OfflineEvent, OfflineSalesSnapshot
from services.event_share_service import EventShareService

MISSING_EVENT_ID = "0123456789abcdef01234567"


class TestTokenGeneration:
    def test_generated_token_matches_public_format(self):
        token = EventShareService.generate_token()

        assert EventShareService.is_valid_token_format(token)

    def test_generated_tokens_are_unique(self):
        tokens = {EventShareService.generate_token() for _ in range(200)}

        assert len(tokens) == 200

    def test_rejects_malformed_tokens(self):
        bad_tokens = [
            None,
            "",
            "short",
            "a" * 42,
            "a" * 44,
            "a" * 42 + "$",
            {"$ne": None},
        ]

        for bad in bad_tokens:
            assert not EventShareService.is_valid_token_format(bad), bad


class TestCreateShareLink:
    def test_stores_the_token_so_the_same_link_can_be_shown_again(self, event):
        result = EventShareService.create_share_link(str(event.id))

        token = result["share_token"]
        stored = OfflineEvent.objects(id=event.id).first()
        assert EventShareService.is_valid_token_format(token)
        assert result["share_token_created_at"] is not None
        assert stored.share_token == token

    def test_regenerating_replaces_the_old_token(self, event):
        first = EventShareService.create_share_link(str(event.id))
        second = EventShareService.create_share_link(str(event.id))

        assert first["share_token"] != second["share_token"]
        assert EventShareService.get_public_report(first["share_token"]) is None
        assert EventShareService.get_public_report(second["share_token"]) is not None

    def test_returns_none_for_missing_event(self):
        assert EventShareService.create_share_link(MISSING_EVENT_ID) is None

    def test_returns_none_for_malformed_event_id(self):
        assert EventShareService.create_share_link("not-an-object-id") is None


class TestGetShareLink:
    def test_returns_the_active_link_every_time(self, event):
        created = EventShareService.create_share_link(str(event.id))

        first = EventShareService.get_share_link(str(event.id))
        second = EventShareService.get_share_link(str(event.id))

        assert first == second == created

    def test_returns_empty_link_when_none_is_active(self, event):
        assert EventShareService.get_share_link(str(event.id)) == {
            "share_token": None,
            "share_token_created_at": None,
        }

    def test_returns_empty_link_after_revoke(self, event):
        EventShareService.create_share_link(str(event.id))
        EventShareService.revoke_share_link(str(event.id))

        assert EventShareService.get_share_link(str(event.id))["share_token"] is None

    def test_returns_none_for_missing_or_malformed_event(self):
        assert EventShareService.get_share_link(MISSING_EVENT_ID) is None
        assert EventShareService.get_share_link("not-an-object-id") is None


class TestUniqueIndexSafety:
    """Regression: an explicit share_token=null on new events collides in the unique index."""

    EVENT_PAYLOAD = {
        "event_name": "Fan Meeting",
        "type": "fan_meeting",
        "event_date": "2026-10-03",
        "session": "Evening",
        "held_country": "HK",
        "held_city": "Hong Kong",
        "venue": "Hall",
        "organizer": "Org",
        "ticket_release": "2026-08-01",
        "ticket_close": "2026-10-02",
    }

    def test_new_events_do_not_store_a_null_share_token(self):
        from services.admin_event_service import OfflineEventService

        created = OfflineEventService.create_event(self.EVENT_PAYLOAD, None)

        raw = OfflineEvent._get_collection().find_one({"event_name": "Fan Meeting"})
        assert created["has_share_link"] is False
        assert "share_token" not in raw
        assert "share_token_created_at" not in raw

    def test_many_events_without_links_can_be_created(self):
        from services.admin_event_service import OfflineEventService

        OfflineEvent.ensure_indexes()
        for _ in range(3):
            OfflineEventService.create_event(self.EVENT_PAYLOAD, None)

        assert OfflineEvent.objects.count() == 3

    def test_app_never_creates_indexes_on_the_live_database(self):
        # Regression: auto-creating the share index on first query made the events list 500
        # on the real DocumentDB. Indexes are created deliberately, not at request time.
        assert OfflineEvent._meta.get("auto_create_index") is False

    def test_events_with_a_leftover_legacy_field_still_load(self, event):
        # Regression: links made by the first (hashed) version left share_token_hash on real
        # events; after the rename, loading them raised FieldDoesNotExist and the list 500'd.
        from services.admin_event_service import OfflineEventService

        OfflineEvent._get_collection().update_one(
            {"_id": event.id}, {"$set": {"share_token_hash": "0" * 64}}
        )

        result = OfflineEventService.get_events(page=1, limit=10, search="")

        assert result["count"] == 1
        assert result["data"][0]["has_share_link"] is False

    def test_index_uses_exists_filter_supported_by_documentdb(self):
        index = next(i for i in OfflineEvent._meta["indexes"] if i["fields"] == ["share_token"])

        assert index["unique"] is True
        assert index["partialFilterExpression"] == {"share_token": {"$exists": True}}


class TestRevokeShareLink:
    def test_revoked_token_no_longer_resolves(self, event):
        token = EventShareService.create_share_link(str(event.id))["share_token"]

        revoked = EventShareService.revoke_share_link(str(event.id))

        assert revoked is True
        assert EventShareService.get_public_report(token) is None
        assert OfflineEvent.objects(id=event.id).first().share_token is None

    def test_returns_false_for_missing_event(self):
        assert EventShareService.revoke_share_link(MISSING_EVENT_ID) is False

    def test_returns_false_for_malformed_event_id(self):
        assert EventShareService.revoke_share_link("not-an-object-id") is False


class TestPublicReport:
    def test_unknown_token_returns_none(self, event):
        EventShareService.create_share_link(str(event.id))

        assert EventShareService.get_public_report(EventShareService.generate_token()) is None

    def test_malformed_token_returns_none(self, event):
        assert EventShareService.get_public_report("../../etc/passwd") is None

    def test_event_without_link_is_not_reachable(self, event):
        assert event.share_token is None
        assert EventShareService.get_public_report(None) is None

    def test_report_contains_event_details(self, event, closed_snapshot):
        token = EventShareService.create_share_link(str(event.id))["share_token"]

        report = EventShareService.get_public_report(token)

        assert report["event"]["event_name"] == "NOVA Fan Meeting Tour"
        assert report["event"]["held_city"] == "Hong Kong"
        assert report["event"]["event_date"] == "2026-10-03T19:00:00"

    def test_report_contains_artist_with_image(self, event):
        token = EventShareService.create_share_link(str(event.id))["share_token"]

        report = EventShareService.get_public_report(token)

        assert report["artists"] == [{
            "artist_en_name": "NOVA",
            "artist_kr_name": "노바",
            "image_url": "https://cdn.example.com/nova.jpg",
        }]

    def test_report_contains_snapshot_figures_and_demographics(self, event, closed_snapshot):
        token = EventShareService.create_share_link(str(event.id))["share_token"]

        snapshot = EventShareService.get_public_report(token)["snapshots"][0]

        assert snapshot["id"] == str(closed_snapshot.id)
        assert snapshot["snapshot_name"] == "Closed"
        assert snapshot["ticket_items"][0]["currency"] == "JPY"
        assert snapshot["ticket_items"][0]["revenue"] == 270000
        assert snapshot["gender_distribution"]["female"] == 60
        assert snapshot["age_distribution"]["age_20s"] == 60

    def test_snapshots_are_newest_first(self, event, closed_snapshot):
        OfflineSalesSnapshot(
            snapshot_name="Week 1",
            observed_at=datetime(2026, 8, 8),
            event_id=str(event.id),
            ticket_items=[],
            created_by="x",
            updated_by="x",
        ).save()
        token = EventShareService.create_share_link(str(event.id))["share_token"]

        names = [s["snapshot_name"] for s in EventShareService.get_public_report(token)["snapshots"]]

        assert names == ["Closed", "Week 1"]

    def test_report_never_exposes_internal_fields(self, event, closed_snapshot):
        token = EventShareService.create_share_link(str(event.id))["share_token"]

        report = EventShareService.get_public_report(token)

        forbidden_event_keys = {
            "id", "event_id", "share_token", "share_token_created_at",
            "created_at", "updated_at", "artist_ids", "artist_id",
        }
        forbidden_snapshot_keys = {
            "event_id", "created_by", "updated_by", "created_at", "updated_at",
        }
        assert forbidden_event_keys.isdisjoint(report["event"])
        assert all("artist_id" not in a and "id" not in a for a in report["artists"])
        for snapshot in report["snapshots"]:
            assert forbidden_snapshot_keys.isdisjoint(snapshot)
        assert token not in str(report)
