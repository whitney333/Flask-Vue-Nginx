from mongoengine import *
from datetime import datetime

class Instagram(Document):
    datetime = DateTimeField(default=datetime.now())
    user_id = StringField(required=True)
    username = StringField(required=True)
    media_count = IntField(required=True)
    follower_count = StringField(required=True)
    following_count = IntField(required=True)
    profile_pic = URLField(required=True)
    threads_follower = IntField(required=True)

class PostDetails(EmbeddedDocument):
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

class InstagramLatest(Document):
    datetime = DateTimeField(default=datetime.now())
    user_id = StringField(required=True)
    posts = ListField(EmbeddedDocumentField(PostDetails))
