import os
import sys
from datetime import datetime

import mongomock
import pytest
from mongoengine import connect, disconnect

BACKEND_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if BACKEND_ROOT not in sys.path:
    sys.path.insert(0, BACKEND_ROOT)

from models.artist_model import Artists  # noqa: E402
from models.event_model import (  # noqa: E402
    AgeDistribution,
    EventArtist,
    GenderDistribution,
    OfflineEvent,
    OfflineSalesSnapshot,
    TicketBenefitItem,
)


@pytest.fixture(autouse=True)
def mongo():
    """Every test runs against a fresh in-memory MongoDB, never a real one."""
    connect(
        "test_db",
        host="mongodb://localhost",
        mongo_client_class=mongomock.MongoClient,
        alias="default",
    )
    yield
    disconnect(alias="default")


@pytest.fixture
def artist():
    # Bypass model validation: only the fields the share feature reads matter here.
    collection = Artists._get_collection()
    inserted = collection.insert_one({
        "english_name": "NOVA",
        "korean_name": "노바",
        "image_url": "https://cdn.example.com/nova.jpg",
    })
    return Artists.objects(id=inserted.inserted_id).first()


@pytest.fixture
def event(artist):
    return OfflineEvent(
        event_name="NOVA Fan Meeting Tour",
        type="fan_meeting",
        artists=[EventArtist(
            artist_id=artist,
            artist_en_name="NOVA",
            artist_kr_name="노바",
        )],
        event_date=datetime(2026, 10, 3, 19, 0),
        session="Evening",
        held_country="HK",
        held_city="Hong Kong",
        venue="Example Hall",
        organizer="Example Promotions",
        ticket_release=datetime(2026, 8, 1),
        ticket_close=datetime(2026, 10, 2),
    ).save()


@pytest.fixture
def closed_snapshot(event):
    return OfflineSalesSnapshot(
        snapshot_name="Closed",
        snapshot_type="closed",
        observed_at=datetime(2026, 10, 3),
        event_id=str(event.id),
        ticket_items=[TicketBenefitItem(
            name="VIP",
            type="ticket",
            currency="JPY",
            price=1500,
            total_quantity=200,
            sold=180,
            refund=0,
            net_sold=180,
            revenue=270000,
            sell_through_rate=90.0,
        )],
        gender_distribution=GenderDistribution(male=40, female=60, unknown=0),
        age_distribution=AgeDistribution(
            age_10s=10, age_20s=60, age_30s=20, age_40s=10, age_50_plus=0,
        ),
        created_by="admin-user-id",
        updated_by="admin-user-id",
    ).save()
