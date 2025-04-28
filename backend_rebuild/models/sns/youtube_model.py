from mongoengine import *
from datetime import datetime

class YoutubeVideo(EmbeddedDocument):
    """
    Embedded field in Youtube document
    """
    published_at = DateTimeField(default=datetime.now())
    title = StringField(required=True)
    thumbnail = URLField(required=True)
    code = StringField(required=True)
    tags = ListField(required=True)
    category_id = StringField(required=True)
    view_count = StringField(required=True)
    like_count = IntField(required=True)
    favorite_count = IntField(required=True)
    comment_count = IntField(required=True)

class Youtube(Document):
    datetime = DateTimeField(default=datetime.now())
    channel_id = StringField(required=True)
    view_count = StringField(required=True)
    subscriber_count = IntField(required=True)
    hidden_subscriber_count = BooleanField(required=True)
    video_count = IntField(required=True)
    channel_hashtag = StringField(required=True)
    video_hashtag = StringField(required=True)
    video = ListField(EmbeddedDocumentField(YoutubeVideo))

class WeeklyTopSongs(EmbeddedDocument):
    rank = StringField(required=True)
    previous_rank = StringField(required=True)
    rank_position = StringField(required=True)
    title = StringField(required=True)
    artist = StringField(required=True)

class YoutubeCharts(Document):
    datetime = DateTimeField(default=datetime.now())
    country = StringField(required=True)
    year = StringField(required=True)
    month = StringField(required=True)
    day = StringField(required=True)
    week = IntField(required=True)
    weekly_top_songs = ListField(EmbeddedDocumentField(WeeklyTopSongs))
