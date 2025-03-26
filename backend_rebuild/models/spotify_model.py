from mongoengine import *
from datetime import datetime

class SpotifyTopCountry(EmbeddedDocument):
    country = StringField(required=True)
    city = StringField(required=True)
    listener = StringField(required=True)

class Track(EmbeddedDocument):
    track = StringField(required=True)
    popularity = IntField(required=True)

class SpotifyRegionTopTrack(EmbeddedDocument):
    region = StringField(required=True)
    country = StringField(required=True)
    tracks = ListField(EmbeddedDocumentField(Track))

class Spotify(Document):
    datetime = datetime.now()
    spotify_id = StringField(required=True)
    name = StringField(required=True)
    genres = ListField(required=True)
    type = StringField(required=True)
    follower = IntField(required=True)
    monthly_listener = IntField(required=True)
    popularity = IntField(required=True)
    top_country = ListField(EmbeddedDocumentField(SpotifyTopCountry))
    top_track = ListField(EmbeddedDocumentField(SpotifyRegionTopTrack))
    popular_track = DictField(required=True)
    image = URLField(required=True)
