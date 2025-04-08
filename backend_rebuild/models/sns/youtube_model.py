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
    video = ListField(EmbeddedDocumentField("YoutubeVideo"))
