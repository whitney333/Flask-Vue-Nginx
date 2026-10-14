from mongoengine import *
from datetime import datetime

class OfflineEvent(Document):
    event_name = StringField(required=True)
    type = StringField(required=True)
    # event datetime
    event_date = DateTimeField(required=True)
    session = StringField(required=True)
    # location
    held_country = StringField(required=True)
    held_city = StringField(required=True)
    venue = StringField(required=True)
    organizer =  StringField(required=True)
    # ticket sales time
    ticket_release = DateTimeField(required=True)
    ticket_close = DateTimeField(required=True)
