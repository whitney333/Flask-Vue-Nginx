from mongoengine import *
from datetime import datetime

class TiktokVideo(Document):
    """
    Embedded field in Tiktok document
    """
    published_at = DateTimeField(default=datetime.now())
    title = StringField(required=True)
    view_count = StringField(required=True)
    like_count = StringField(required=True)
    comment_count = StringField(required=True)
    share_count = StringField(required=True)
    save_count = StringField(required=True)
    tags = ListField
    url = URLField(required=True)
    thumbnail = URLField(required=True)


class Tiktok(Document):
    datetime = DateTimeField(default=datetime.now())
    tiktok_id = StringField(required=True, db_field="tiktok_id")
    follower = StringField()
    like = StringField()
    hashtag = StringField()
