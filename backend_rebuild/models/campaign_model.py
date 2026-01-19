from mongoengine import *
from datetime import datetime

class CampaignPost(EmbeddedDocument):
    "Embedded document for post details"
    kol_account = StringField(required=True)
    platform = StringField(required=True)
    status = StringField(required=True)
    type = StringField(required=True)
    artist = StringField(required=True) # promo IP
    content = StringField(required=True)
    used_hashtag = ListField()
    hashtag_reach = IntField()
    target_country = StringField(required=True)
    url = StringField(required=True)
    post_created_at = DateTimeField(required=True)
    cost = IntField(required=True)
    reach = IntField(required=True)
    one_hour_view = IntField()
    twentyfour_hour_view = IntField()
    latest_view = IntField()
    reaction = IntField()
    engagement = StringField()
    cost_per_reach = StringField(null=True)
    cost_per_view = StringField(null=True)
    notes = StringField(null=True)

class CampaignTotalCountry(EmbeddedDocument):
    name = StringField(required=False)
    count = IntField(required=False)
    region = StringField(required=False)

class CampaignTotalRegion(EmbeddedDocument):
    name = StringField(required=False)
    count = IntField(required=False)

class CampaignTotalPlatform(EmbeddedDocument):
    name = StringField(required=False)
    count = IntField(required=False)

class Campaign(Document):
    campaign_id = StringField(required=True, unique=True)
    user_id = ReferenceField(Users, required=True)
    created_at = DateTimeField(default=datetime.now())
    approved_at = DateTimeField(null=True)
    status = StringField(required=True)
    cancelled_at = DateTimeField(null=True)
    cancelled_by = StringField()
    artist_id = LazyReferenceField(Artists, required=True)
    artist_en_name = StringField(required=True)
    artist_kr_name = StringField(required=True)
    platform = ListField(required=True)
    region = ListField(required=True)
    budget = StringField(required=True)
    post = ListField(EmbeddedDocumentField(CampaignPost), default=lambda: [])
    info = DictField(required=True)
    total_cost = FloatField(null=True, required=False)
    total_reach = IntField(null=True, required=False)
    total_country = ListField(EmbeddedDocumentField(CampaignTotalCountry), default=lambda: [])
    total_region = ListField(EmbeddedDocumentField(CampaignTotalRegion), default=lambda: [])
    total_platform = ListField(EmbeddedDocumentField(CampaignTotalPlatform), default=lambda: [])