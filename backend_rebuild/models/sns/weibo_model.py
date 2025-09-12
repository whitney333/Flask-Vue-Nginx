from mongoengine import *
from datetime import datetime

class Weibo(Document):
    datetime = DateTimeField(default=datetime.now())
    id = StringField(required=True)
    follower = IntField(required=True)
    statuses_count = IntField(required=True)
