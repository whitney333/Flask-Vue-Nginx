from mongoengine import *
from datetime import datetime


class SpotifyTopCountry(EmbeddedDocument):
    country = StringField(required=True)
    city = StringField(required=True)
    listener = StringField(required=True)

class Track(EmbeddedDocument):
    track = StringField(required=True)
    popularity = IntField(required=True)

class TopTrack(EmbeddedDocument):
    """
    Spotify region top tracks
    """
    region = StringField(required=True)
    country = StringField(required=True)
    tracks = ListField(EmbeddedDocumentField(Track))

class Spotify(Document):
    datetime = DateTimeField(default=datetime.now())
    spotify_id = StringField(required=True, db_field="spotify_id")
    artist = StringField()
    name = StringField(required=True)
    genre = ListField(required=True)
    type = StringField(required=True)
    follower = IntField(required=True)
    monthly_listener = IntField(required=True)
    popularity = IntField(required=True)
    top_country = ListField(EmbeddedDocumentField(SpotifyTopCountry))
    top_track = ListField(EmbeddedDocumentField(TopTrack))
    popular_track = DictField(required=True)
    image = URLField(required=True)

class WeeklyTopSongs(EmbeddedDocument):
    rank = StringField(required=True)
    title = StringField(required=True)
    artist_id = StringField(required=True)
    artist = StringField(required=True)
    rank_change = StringField(required=True)
    peak = StringField(required=True)
    streak = StringField(required=True)
    stream = StringField(required=True)

class SpotifyOst(Document):
    week = IntField(required=True)
    datetime = DateTimeField(default=datetime.now())
    country = StringField(required=True)
    track = StringField(required=True)
    track_code = StringField(required=True)
    album = StringField(required=True)
    album_code = StringField(required=True)
    artist = StringField(required=True)
    artist_code = StringField(required=True)
    release_date = StringField(required=True)
    added_at = StringField(required=True)
    popularity = IntField(required=True)
    thumbnail = URLField(required=True)
    play_counts = StringField(required=True)

class SpotifyCharts(Document):
    datetime = DateTimeField(default=datetime.now())
    country = StringField(required=True)
    year = StringField(required=True)
    month = StringField(required=True)
    day = StringField(required=True)
    week = IntField(required=True)
    weekly_top_songs = ListField(EmbeddedDocumentField(WeeklyTopSongs))
