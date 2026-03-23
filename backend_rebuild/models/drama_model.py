from mongoengine import *
from datetime import datetime
from models.artist_model import Artists


class Drama(Document):
    meta = {'collection': 'drama'}
    drama_id = StringField(required=True, db_field="drama_id")
    drama_sequence = IntField(required=True, db_field="drama_sequence")
    name = StringField(required=True, db_field="name")
    name_in_korean = StringField(required=True, db_field="name_in_korean")
    onair_date = DateTimeField(db_field="onair_date")
    broadcast_day = ListField(StringField(db_field="broadcast_day"))
    broadcast_time = DateTimeField(db_field="broadcast_time")
    broadcast_year = IntField(required=True, db_field="broadcast_year")
    country = StringField(required=True, db_field="country")
    episode = IntField(required=True, db_field="episode")
    special_episode = IntField(db_field="special_episode")
    finale = DateTimeField(db_field="finale")
    genre = ListField(StringField(db_field="genre", required=True))
    type = StringField(required=True, db_field="type")
    language = StringField(required=True, db_field="language")
    premiere_channel = ListField(StringField(db_field="premiere_channel"))
    streaming = ListField(StringField(db_field="streaming"))
    director = ListField(StringField(db_field="director"))
    production = ListField(StringField(db_field="production"))
    screenwriter = ListField(StringField(db_field="screenwriter"))
    starring = ListField(ReferenceField('Artists'))
    thumbnail_url = StringField(db_field="thumbnail")
