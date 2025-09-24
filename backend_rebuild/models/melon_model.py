from mongoengine import *
from datetime import datetime

class Melon(Document):
    datetime = DateTimeField(default=datetime.now(), db_field="datetime")
    # artist melon_id
    melon_id = StringField(required=True, db_field="melon_id")
    follower = StringField(required=True, db_field="follower")
