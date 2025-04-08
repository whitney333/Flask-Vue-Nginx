from mongoengine import *
from datetime import datetime

class Instagram(Document):
    datetime = DateTimeField(default=datetime.now()),
    pk = StringField(required=True),
    username = StringField(required=True),
    media_count = IntField(required=True),
    follower_count = StringField(required=True),
    following_count = IntField(required=True),
    profile_pic = URLField(required=True),
    thread_follower = IntField(required=True)

class InstagramPost(Document):
    pass
