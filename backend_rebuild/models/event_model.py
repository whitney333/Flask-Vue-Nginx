from mongoengine import *
from datetime import datetime
from models.artist_model import Artists


class EventArtist(EmbeddedDocument):
    artist_id = LazyReferenceField(Artists, required=True)
    artist_en_name = StringField(required=True)
    artist_kr_name = StringField(default="")

class OfflineEvent(Document):
    meta = {
        'collection': 'offline_event',
        # Never create indexes from the app at request time: doing so on the live DocumentDB
        # failed and broke the events list. Create the index below once, deliberately
        # (OfflineEvent.ensure_indexes() from a maintenance shell). Lookups work without it.
        'auto_create_index': False,
        # Ignore fields stored by earlier code (e.g. share_token_hash from the first share-link
        # version) instead of failing to load the event: one stray field broke the whole list.
        'strict': False,
        'indexes': [
            # Public share-link lookups. Partial on $exists (supported by MongoDB and
            # AWS DocumentDB): events without a link have no field and are not indexed.
            {
                'fields': ['share_token'],
                'unique': True,
                'partialFilterExpression': {'share_token': {'$exists': True}},
            },
        ],
    }

    event_name = StringField(required=True)
    type = StringField(required=True)
    artists = ListField(
        EmbeddedDocumentField(EventArtist),
        default=list,
    )
    # event datetime
    event_date = DateTimeField(required=True)
    session = StringField(required=True)
    # location
    held_country = StringField(required=True)
    held_city = StringField(required=True)
    venue = StringField(required=True)
    organizer =  StringField(required=True)
    # ticket sales time
    ticket_release = DateTimeField(required=True)
    ticket_close = DateTimeField(required=True)
    # Public share-link token (absent = no active link). Stored as-is so admins can copy the
    # same link again; it only guards this event's report, which lives in this same DB.
    # Must NOT be null=True: an explicit null would be indexed by the partial $exists index
    # and collide across events. Revoke uses $unset so the field disappears.
    share_token = StringField()
    share_token_created_at = DateTimeField()
    created_at = DateTimeField(default=datetime.now)
    updated_at = DateTimeField(default=datetime.now)
    share_token_created_at = DateTimeField(
        required=False,
        null=True,
        default=None
    )

    share_token_hash = StringField(
        required=False,
        null=True,
        default=None
    )

class TicketBenefitItem(EmbeddedDocument):
    name = StringField(required=True)
    type = StringField(required=True, choices=['ticket', 'benefit'])
    currency = StringField(required=True)
    price = FloatField(default=0.0)
    total_quantity = IntField(default=0)
    sold = IntField(default=0)
    refund = IntField(default=0)
    # calculated fields
    net_sold = IntField(default=0)
    revenue = IntField(default=0)
    sell_through_rate = FloatField(default=0.0)

class GenderDistribution(EmbeddedDocument):
    male = FloatField(default=0.0, min_value=0, max_value=100)
    female = FloatField(default=0.0, min_value=0, max_value=100)
    unknown = FloatField(default=0.0, min_value=0, max_value=100)

class AgeDistribution(EmbeddedDocument):
    age_10s = FloatField(default=0.0, min_value=0, max_value=100)
    age_20s = FloatField(default=0.0, min_value=0, max_value=100)
    age_30s = FloatField(default=0.0, min_value=0, max_value=100)
    age_40s = FloatField(default=0.0, min_value=0, max_value=100)
    age_50_plus = FloatField(default=0.0, min_value=0, max_value=100)

class OfflineSalesSnapshot(Document):
    meta = {'collection': 'offline_sales_snapshot'}

    snapshot_name = StringField(required=True)
    snapshot_type = StringField(choices=['custom', 'closed'], required=False, null=True)
    observed_at = DateTimeField(required=True)
    event_id = StringField(required=True)
    ticket_items = ListField(EmbeddedDocumentField('TicketBenefitItem'))
    created_by = StringField(required=True)
    created_at = DateTimeField(default=datetime.now)
    updated_by = StringField(required=True)
    updated_at = DateTimeField(default=datetime.now)

    # Final snapshot only
    gender_distribution = EmbeddedDocumentField(
        GenderDistribution,
        required=False,
        null=True,
    )
    age_distribution = EmbeddedDocumentField(
        AgeDistribution,
        required=False,
        null=True,
    )
