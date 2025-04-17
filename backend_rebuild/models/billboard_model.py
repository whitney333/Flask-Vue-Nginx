from mongoengine import *
from datetime import datetime

class Track(EmbeddedDocumentField):
    title = StringField(required=True)
    ranking = StringField(required=True)
    rank_position = StringField(required=True)
    peak_position = StringField(required=True)
    weeks_on_chart = StringField(required=True)
    artist = StringField(required=True)

class BillboardCharts(Document):
    datetime = DateTimeField(default=datetime.now())
    year = StringField(required=True)
    month = StringField(required=True)
    day = StringField(required=True)
    week = IntField(required=True)
    date = StringField(required=True)
    data = ListField(EmbeddedDocumentField(Track))
