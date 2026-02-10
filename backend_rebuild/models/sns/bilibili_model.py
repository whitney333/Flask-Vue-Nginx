from mongoengine import *
from datetime import datetime

class PostDetails(EmbeddedDocument):
    bvid = StringField(required=True)
    aid = IntField(required=True)
    title = StringField(required=True)
    image = URLField(required=True)
    image_hash = StringField()
    upload_date = StringField(required=True)
    view = IntField()
    danmu = IntField()
    comment = IntField()
    collect = IntField()
    coin = IntField()
    share = IntField()
    like = IntField()

class Bilibili(Document):
    datetime = DateTimeField(default=datetime.now())
    user_id = StringField(required=True)
    follower = IntField(required=True)
    data = ListField(EmbeddedDocumentField(PostDetails))
