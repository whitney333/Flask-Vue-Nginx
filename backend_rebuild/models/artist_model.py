'''
updated: 2025-08-04
artist model
- tenant_id: ReferenceField(Tenant)
- english_name: string
- korean_name: string
- debut_year: int
- nation: string (reference to Nation)
- pronouns: string
- type: list of strings
- birth: datetime
- fandom: string
- instagram_id: ReferenceField(Instagram)
- threads: boolean
- youtube_id: ReferenceField(Youtube)
- tiktok_id: ReferenceField(Tiktok)
- spotify_id: ReferenceField(Spotify)
- melon_id: ReferenceField(Melon)
- bilibili_id: ReferenceField(Bilibili)
- image_url: string
'''

from mongoengine import *
from datetime import datetime
from models.tenant_model import Tenant
from models.instagram_model import Instagram
from models.youtube_model import Youtube
from models.tiktok_model import Tiktok
from models.spotify_model import Spotify
from models.melon_model import Melon
from models.bilibili_model import Bilibili
from enum import Enum

class Nation(Enum):
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

class Artist(Document):
    tenant_id = ReferenceField(Tenant, required=True)
    artist_id = StringField(required=True)
    english_name = StringField(required=True)
    korean_name = StringField(required=True)
    debut_year = IntField()
    nation = StringField(required=True)
    pronouns = StringField(required=True)
    type = ListField(StringField(), required=True)
    birth = DateTimeField()
    fandom = StringField()
    belong_group = ListField()
    threads = BooleanField()
    instagram_id = StringField(required=False, null=True)
    youtube_id = StringField(required=False, null=True)
    tiktok_id = StringField(required=False, null=True)
    spotify_id = StringField(required=False, null=True)
    melon_id = StringField(required=False, null=True)
    genie_id = StringField(required=False, null=True)
    apple_id =  StringField(required=False, null=True)
    bilibili_id = StringField(required=False, null=True)
    weibo_id = StringField(required=False, null=True)
    image_url = StringField()
    instagram_user = StringField(required=False, null=True)
    is_active = BooleanField(default=True)