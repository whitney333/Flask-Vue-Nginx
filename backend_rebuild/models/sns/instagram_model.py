from mongoengine import *
from datetime import datetime
from models.artist_model import Artist

class Instagram(Document):
    artist = ReferenceField(Artist)
    datetime = DateTimeField(default=datetime.now())
    user_id = StringField(required=True)
    username = StringField(required=True)
    media_count = IntField(required=True)
    follower_count = StringField(required=True)
    following_count = IntField(required=True)
    profile_pic = URLField(required=True)

    # Threads integration
    has_threads = BooleanField(default=False)
    threads_username = StringField()
    threads_follower = IntField()

    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)

class InstagramDailySnapshot(Document):
    artist = ReferenceField(Artist)
    datetime = DateTimeField(default=datetime.now())
    user_id = StringField(required=True)
    media_count = IntField(required=True)
    follower_count = IntField(required=True)
    following_count = IntField(required=True)
    total_likes = IntField(required=True)
    total_comments = IntField(required=True)
    total_views = IntField(required=True)
    total_play_count = IntField(required=True)
    total_view_count = IntField(required=True)
    total_engagement_rate = FloatField(required=True)
    posts = ListField(EmbeddedDocumentField(PostDetails))

class PostDetails(EmbeddedDocument):
    artist = ReferenceField(Artist)
    pk = StringField()
    id = StringField(required=True)
    user_pk = StringField(required=True)
    username = StringField(required=True)
    code = StringField(required=True)
    taken_at = DateTimeField(default=datetime.now())
    media_type = IntField(required=True)
    product_type = StringField(required=True)
    comment_count = IntField(required=True)
    like_count = IntField(required=True)
    play_count =IntField()
    view_count = IntField()
    caption_text = StringField(required=True)
    thumbnail = URLField(required=True)
    video_url = URLField(required=True)
    # engagement_rate = (like_count + comment_count) / follower_count
    engagement_rate = FloatField(required=True)
    hashtags = ListField(StringField())
    hashtags_count = IntField(required=True)

