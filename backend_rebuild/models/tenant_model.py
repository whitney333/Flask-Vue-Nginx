from mongoengine import *
from datetime import datetime

class Tenant(Document):
    tenant_id = StringField(required=True, unique=True)
    tenant_name = StringField(required=True)
    created_at = DateTimeField(required=True)
    updated_at = DateTimeField(required=True)
    # website = StringField(required=True)
    # email = StringField(required=True)
