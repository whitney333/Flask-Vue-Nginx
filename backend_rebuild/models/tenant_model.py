from mongoengine import *
from datetime import datetime

class Tenant(Document):
    tenant_id = IntField(required=True, unique=True)
    tenant_name = StringField(required=True)
    created_at = DateTimeField(required=True, default=datetime.now())
    updated_at = DateTimeField(null=True)
    website = StringField(sparse=True)
    email = EmailField(unique=True, sparse=True)
    status = StringField(default="active")
    closed_at = DateTimeField(null=True)
