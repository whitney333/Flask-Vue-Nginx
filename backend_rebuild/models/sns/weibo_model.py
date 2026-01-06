from mongoengine import *
from datetime import datetime

class Weibo(Document):
    datetime = DateTimeField(default=datetime.utcnow())
    weibo_id = StringField(required=True)
    follower = IntField(required=True)
    statuses_count = IntField(required=True)
    share_count = IntField(default=0)
    like_count = IntField(default=0)
    comment_count = IntField(default=0)
    total_eng_count = IntField(default=0)
