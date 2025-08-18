from mongoengine import *
from datetime import datetime
from .tenant_model import Tenant
from models.sns.instagram_model import Instagram
from models.sns.youtube_model import Youtube
from models.sns.tiktok_model import Tiktok
from models.sns.bilibili_model import Bilibili
from models.melon_model import Melon
from models.spotify_model import Spotify
from enum import Enum

class Nation(Enum):
    # nation list for selection
    Taiwan = "TW"
    Hong_Kong = "HK"
    Japan = "JP"
    South_Korea = "KR"
    Thailand = "TH"
    Vietnam = "VN"
    Philippines = "PH"
    Indonesia = "ID"
    United_States = "US"
    Canada = "CA"
    Brazil = "BR"
    Mexico = "MX"
    United_Kingdom = "GB"
    Germany = "DE"
    France = "FR"
    Spain = "ES"
    Italy = "IT"
    Australia = "AU"

class Artists(Document):
    tenant_id = ReferenceField(Tenant, required=True)
    artist_id = StringField(required=True)
    english_name = StringField(required=True)
    korean_name = StringField(required=True)
    debut_year = IntField()
    nation = StringField(required=True)
    pronouns = StringField(required=True)
    type = ListField(required=True)
    birth = DateTimeField()
    fandom = StringField()
    belong_group = ListField()
    threads = BooleanField()
    instagram_id = ReferenceField("Instagram")
    youtube_id = StringField("Youtube")
    tiktok_id = ReferenceField("Tiktok")
    spotify_id = ReferenceField("Spotify")
    melon_id = StringField("Melon")
    genie_id = StringField()
    bilibili_id = ReferenceField("Bilibili")
    weibo_id = StringField()
    image_url = URLField()
    # instagram_id = StringField()
    instagram_user = StringField()
    # youtube_id = StringField()
    # tiktok_id = StringField()
    # spotify_id = StringField()
    # melon_id = StringField()
    # genie_id = StringField()
    # bilibili_id = StringField()
    # qq_id = StringField()
    # weibo_id = StringField()

