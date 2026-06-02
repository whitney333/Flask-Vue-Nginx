from mongoengine import *
from datetime import datetime
from .artist_model import Artists


class ArtistPopularity(Document):
    artist_id = ReferenceField(Artists)
    english_name = StringField()
    korean_name = StringField()
    type = ListField(StringField())
    image = StringField()
    country = StringField(default="GLOBAL")

    year = IntField(required=True)
    week = IntField(required=True)

    music_score = FloatField(default=0)
    sns_score = FloatField(default=0)
    drama_score = FloatField(default=0)

    popularity_score = FloatField(default=0)
    rank = IntField(min_value=1)
    updated_at = DateTimeField(default=datetime.utcnow)
    created_at = DateTimeField(default=datetime.utcnow)

    meta = {
        "collection": "artist_popularity",
        "indexes": [
            {
                "fields": ["artist_id", "country", "year", "week"],
                "unique": True
            },
            {
                "fields": ["country", "year", "week", "-popularity_score"]
            },
            {
                "fields": ["country", "year", "week", "-music_score"]
            },
            {
                "fields": ["country", "year", "week", "-sns_score"]
            },
            {
                "fields": ["country", "year", "week", "-drama_score"]
            }
        ]
    }
