from mongoengine import *
from datetime import datetime
from .tenant_model import Tenant
from .artist_model import Artists

class Users(Document):
    firebase_id = StringField(required=True, unique=True)
    name = StringField(required=True)
    image_url = URLField(default=None)
    email = EmailField(required=True, unique=True)
    # [user, admin] role
    admin = BooleanField(required=True)
    # user belongs to which company
    tenant = ReferenceField(Tenant, required=True, reverse_delete_rule=CASCADE)
    # artist list which the user follows 
    followed_artist = ListField(ReferenceField(Artists))
