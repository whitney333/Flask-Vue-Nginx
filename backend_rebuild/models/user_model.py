'''
updated: 2025-08-04
user model
- firebase_id: string
- name: string
- image_url: string
- email: string
- followed_artist: list of artist ids (reference to artist)
- tenant: string (reference to tenant)
- admin: boolean
'''
from mongoengine import *
from datetime import datetime
from models.artists_model import Artists
from models.tenant_model import Tenant

class User(Document):
    firebase_id = StringField(required=True, unique=True)
    name = StringField(required=True)
    image_url = URLField(required=True)
    email = EmailField(required=True, unique=True)
    followed_artist = ListField(ReferenceField(Artist))
    tenant = ReferenceField(Tenant, required=True)
    admin = BooleanField(required=True)
