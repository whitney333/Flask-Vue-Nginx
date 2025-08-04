'''
updated: 2025-08-04
tenant model
- tenant_name: string
- tenant_created_at: datetime
- tenant_updated_at: datetime
- tenant_website: string
- tenant_email: string
'''

from mongoengine import *

class Tenant(Document):
    tenant_name = StringField(required=True)
    tenant_created_at = DateTimeField(required=True)
    tenant_updated_at = DateTimeField(required=True)
    tenant_website = StringField(required=True)
    tenant_email = StringField(required=True)