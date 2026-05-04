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
    meta = {"strict": False}
    id = StringField(required=True, db_field="id")
    type = StringField(required=True, db_field="type")
    product_type = StringField(required=True, db_field="productType")
    shortcode = StringField(required=True, db_field="code")
    user_id = StringField(required=True, db_field="ownerId")
    username = StringField(required=True, db_field="ownerUsername")
    taken_at = DateTimeField(default=datetime.now(), db_field="timestamp")
    comment_count = IntField(required=True, db_field="commentsCount")
    like_count = IntField(required=True, db_field="likesCount")
    view_count = IntField(default=None, db_field="videoViewCount")
    caption_text = StringField(required=True, db_field="caption")
    thumbnail = StringField(required=True, db_field="displayUrl")
    post_url = StringField(default=None, db_field="url")
    hashtag = ListField(default=None, db_field="hashtags")

class InstagramLatest(Document):
    datetime = DateTimeField(default=datetime.now())
    user_id = StringField(required=True)
    posts = ListField(EmbeddedDocumentField(PostDetails))
