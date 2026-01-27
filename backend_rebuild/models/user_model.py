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
    tenant = ReferenceField(Tenant, required=True)
    # artist list which the user follows 
    followed_artist = ListField(ReferenceField(Artists))
    created_at = DateTimeField(null=True)
    last_login_at = DateTimeField(null=True)
    # membership
    is_premium = BooleanField(default=False)
    plan = StringField(choices=["free", "monthly", "yearly"], default="free")
    premium_expired_at = DateTimeField(null=True)
    # Stripe
    stripe_customer_id = StringField()
    stripe_subscription_id = StringField()
