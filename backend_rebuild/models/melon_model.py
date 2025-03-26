from mongoengine import *
from datetime import datetime

class Melon(Document):
    datetime = DateTimeField(default=datetime.now(), db_field="datetime")
    id = StringField(required=True, db_field="id")
    follower = StringField(required=True, db_field="follower")
