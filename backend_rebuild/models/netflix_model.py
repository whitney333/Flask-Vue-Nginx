from mongoengine import *
from datetime import datetime


class NetflixCharts(Document):
    datetime = DateTimeField(default=datetime.now())
    country = StringField(required=True)
    week = IntField(required=True)
    rank = IntField(required=True)
    name = StringField(required=True)
    weeks_on_chart = StringField(required=True)
    views = StringField()
    runtime = StringField()
    hours_viewed = StringField()
