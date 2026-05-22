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

    updated_at = DateTimeField(default=datetime.utcnow)
    created_at = DateTimeField(default=datetime.utcnow)

    meta = {
        "collection": "artist_popularity",
        "indexes": [
            ("country", "year", "week", "-overall_score"),
            ("country", "year", "week", "-music_score"),
            ("country", "year", "week", "-sns_score"),
            ("country", "year", "week", "-drama_score"),
            ("artist_id", "country", "year", "week"),
            {"fields": [
                    "artist_id",
                    "country",
                    "year",
                    "week"
                ],
                "unique": True
            }
        ]
    }

class ArtistMusicScore(DynamicDocument):
    meta = {
        "collection": "artist_music_score",
        "strict": False,
    }
    artist_id = ReferenceField('Artist', required=True)
    english_name = StringField()
    korean_name = StringField()
    type = ListField(StringField(), required=True)
    image = URLField()

    # Time and region
    year = IntField(required=True)
    week = IntField(required=True)
    country = StringField(required=True)

    # Scores
    spotify_score = FloatField(default=0)
    spotify_normalized = FloatField(default=0)
    youtube_score = FloatField(default=0)
    youtube_normalized = FloatField(default=0)
    billboard_score = FloatField(default=0)
    billboard_normalized = FloatField(default=0)

    # Timestamps
    updated_at = DateTimeField(default=datetime.utcnow)

    # Final score
    music_score = FloatField(default=0)


class ArtistSnsScore(DynamicDocument):
    meta = {
        "collection": "artist_sns_score",
        "strict": False,
    }


class ArtistDramaScore(DynamicDocument):
    meta = {
        "collection": "artist_drama_score",
        "strict": False,
    }
