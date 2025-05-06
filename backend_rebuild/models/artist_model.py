from mongoengine import *
from datetime import datetime


class Artists(Document):
    artist_id = StringField(required=True)
    english_name = StringField(required=True)
    korean_name = StringField(required=True)
    debut_year = StringField()
    nation = StringField(required=True)
    pronouns = StringField(required=True)
    type = ListField(required=True)
    birth = DateTimeField()
    fandom = StringField()
    belong_group = ListField()
    instagram_id = StringField()
    instagram_user = StringField()
    threads = BooleanField()
    youtube_id = StringField()
    tiktok_id = StringField()
    spotify_id = StringField()
    melon_id = StringField()
    genie_id = StringField()
    bilibili_id = StringField()
    qq_id = StringField()
    weibo_id = StringField()
    image = URLField()
