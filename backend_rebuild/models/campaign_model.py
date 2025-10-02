from mongoengine import *
from models.artist_model import Artists
from models.user_model import Users
from datetime import datetime

class CampaignPost(EmbeddedDocument):
    "Embedded document for post details"
    kol_account = StringField(required=True)
    platform = StringField(required=True)
    content_type = StringField(required=True)
    promo = StringField(required=True) # promo IP
    used_hashtag = ListField()
    hashtag_reach = IntField()
    target_region = StringField(required=True)
    post_url = StringField(required=True)
    post_date = DateTimeField(required=True)
    cost = Decimal128Field(required=True)
    reach = IntField(required=True)
    one_hour_view = IntField()
    twentyfour_hr_view = IntField()
    latest_view = IntField()
    reaction = IntField()
    engagement = StringField()
    cost_per_reach = Decimal128Field()
    cost_per_view = Decimal128Field()


class Campaign(Document):
    campaign_id = StringField(required=True, unique=True)
    user_id = ReferenceField(Users, required=True)
    created_at = DateTimeField(default=datetime.now())
    artist = ReferenceField(Artists, required=True)
    platform = ListField(required=True)
    region = ListField(required=True)
    budget = StringField(required=True)
    post = ListField(EmbeddedDocumentField(CampaignPost))
