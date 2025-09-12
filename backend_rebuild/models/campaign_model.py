from mongoengine import *
from datetime import datetime

class CampaignPost(EmbeddedDocument):
    "Embedded document for post details"
    title = StringField(required=True)
    description = StringField()
    text = StringField()
    url = URLField()
    file = BinaryField()

class Campaign(Document):
    created_at = DateTimeField(default=datetime.now())
    user_id = StringField(required=True)
    platform = ListField(required=True)
    region = ListField(required=True)
    budget = StringField(required=True)
    post = EmbeddedDocumentField(CampaignPost)
