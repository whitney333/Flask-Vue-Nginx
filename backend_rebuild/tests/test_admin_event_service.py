"""Admin event list: artist names come from one batched query, not one fetch per artist."""
from datetime import datetime

import pytest
from bson import ObjectId
from mongoengine.base.datastructures import LazyReference

from models.artist_model import Artists
from models.event_model import EventArtist, OfflineEvent
from services.admin_event_service import OfflineEventService


def _make_artist(en: str, kr: str, image_url: str = None) -> Artists:
    inserted = Artists._get_collection().insert_one(
        {"english_name": en, "korean_name": kr, "image_url": image_url}
    )
    return Artists.objects(id=inserted.inserted_id).first()


def _make_event(name: str, artist_refs) -> OfflineEvent:
    return OfflineEvent(
        event_name=name,
        type="fan_meeting",
        artists=[
            EventArtist(artist_id=ref, artist_en_name=en, artist_kr_name=kr)
            for ref, en, kr in artist_refs
        ],
        event_date=datetime(2026, 10, 3, 19, 0),
        session="Evening",
        held_country="HK",
        held_city="Hong Kong",
        venue="Venue",
        organizer="Organizer",
        ticket_release=datetime(2026, 9, 1),
        ticket_close=datetime(2026, 10, 2),
    ).save()


@pytest.fixture
def no_per_artist_fetch(monkeypatch):
    def _fail(self, *args, **kwargs):
        raise AssertionError("per-artist fetch() used: this is the N+1 query")

    monkeypatch.setattr(LazyReference, "fetch", _fail)


def test_list_uses_current_artist_names_without_per_artist_fetch(no_per_artist_fetch):
    renamed = _make_artist("NOVA (new)", "노바 new")
    other = _make_artist("LUMEN", "루멘")
    _make_event("A", [(renamed, "NOVA old", "노바 old")])
    _make_event("B", [(other, "LUMEN", "루멘"), (renamed, "NOVA old", "노바 old")])

    result = OfflineEventService.get_events(page=1, limit=10)

    names = {e["event_name"]: [a["artist_en_name"] for a in e["artists"]] for e in result["data"]}
    assert names == {"A": ["NOVA (new)"], "B": ["LUMEN", "NOVA (new)"]}
    first = next(e for e in result["data"] if e["event_name"] == "A")
    assert first["artist_id"] == str(renamed.id)
    assert first["artist_kr_name"] == "노바 new"


def test_list_falls_back_to_embedded_names_when_artist_is_gone(no_per_artist_fetch):
    missing_id = ObjectId()
    _make_event("Ghost", [(missing_id, "Old Name", "옛 이름")])

    result = OfflineEventService.get_events(page=1, limit=10)

    artist = result["data"][0]["artists"][0]
    assert artist == {
        "id": str(missing_id),
        "artist_id": str(missing_id),
        "artist_en_name": "Old Name",
        "artist_kr_name": "옛 이름",
        "image": None,
    }


def test_single_event_serialization_still_resolves_current_names(no_per_artist_fetch):
    renamed = _make_artist("NOVA (new)", "노바 new")
    event = _make_event("A", [(renamed, "NOVA old", "노바 old")])

    data = OfflineEventService.serialize_event(event)

    assert data["artist_en_name"] == "NOVA (new)"
    assert data["artist_ids"] == [str(renamed.id)]


def test_event_artists_include_their_image_so_the_detail_page_needs_no_full_artist_list(
    no_per_artist_fetch,
):
    artist = _make_artist("NOVA", "노바", "https://cdn.example.com/nova.jpg")
    event = _make_event("A", [(artist, "NOVA", "노바")])

    data = OfflineEventService.serialize_event(event)

    assert data["artists"][0]["image"] == "https://cdn.example.com/nova.jpg"
