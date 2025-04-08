from mongoengine import *
from datetime import datetime

class User(Document):
    firebase_id = StringField(required=True, unique=True)
    name = StringField(required=True)
    company_name = StringField(required=True)
    artist_name = StringField(required=True)
    image_url = URLField(required=True)
    email = EmailField(required=True, unique=True)
    user_id = StringField()
