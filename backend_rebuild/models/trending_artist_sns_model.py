from mongoengine import *
from datetime import datetime
from models.artist_model import Artists


class TrendingArtistSnsScore(Document):
    meta = {
        "collection": "artist_sns_score",
        "indexes": [
            ("year", "week"),
            ("artist_id", "year", "week")
        ]
    }

    artist_id = ReferenceField(Artists)
    english_name = StringField()
    korean_name = StringField()
    type = ListField(StringField())
    image = StringField()
    year = IntField()
    week = IntField()
    instagram_score = FloatField()
    instagram_normalized = FloatField()
    youtube_score = FloatField()
    youtube_normalized = FloatField()
    tiktok_score = FloatField()
    tiktok_normalized = FloatField()
    updated_at = DateTimeField(default=datetime.utcnow)
    sns_score = FloatField()
