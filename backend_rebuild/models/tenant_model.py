from mongoengine import *
from datetime import datetime

class Tenant(Document):
    tenant_id = IntField(required=True, unique=True)
    tenant_name = StringField(unique=True, required=True)
    created_at = DateTimeField(required=True, default=datetime.now())
    updated_at = DateTimeField(null=True)
    website = StringField(sparse=True)
    email = EmailField(sparse=True, null=True)
    status = StringField(default="active")
    closed_at = DateTimeField(null=True)
