from mongoengine import *
from datetime import datetime
from models.artist_model import Artists


class TrendingArtistMusicScore(Document):
    meta = {
        "collection": "artist_music_score",
        "indexes": [
            ("country", "year", "week"),
            ("artist_id", "country", "year", "week")
        ]
    }

    artist_id = ReferenceField(Artists)
    english_name = StringField()
    korean_name = StringField()
    type = ListField(StringField())
    image = StringField()
    year = StringField()
    week = IntField()
    country = StringField()
    spotify_score = FloatField()
    spotify_normalized = FloatField()
    youtube_score = FloatField()
    youtube_normalized = FloatField()
    billboard_score = FloatField()
    billboard_normalized = FloatField()
    updated_at = DateTimeField(default=datetime.utcnow)
    music_score = FloatField()
