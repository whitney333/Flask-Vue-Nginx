from mongoengine import *
from datetime import datetime

class DirectorName(EmbeddedDocument):
    name = StringField(required=True)

class ProductionName(EmbeddedDocument):
    name = StringField(required=True)

class StarringId(EmbeddedDocument):
    mid = StringField(required=True)

class PremiereChannel(EmbeddedDocument):
    name = StringField()

class Screenwriter(EmbeddedDocument):
    name = StringField()

class Streaming(EmbeddedDocument):
    name = StringField()

class Drama(Document):
    id = StringField(required=True)
    name = StringField(required=True)
    name_in_korean = StringField(required=True)
    onair_date = DateTimeField()
    broadcast_day = StringField()
    broadcast_time = StringField()
    broadcast_year = IntField(required=True)
    country = StringField(required=True)
    episode = StringField(required=True)
    special_episode = StringField()
    finale = DateTimeField()
    genre = ListField(required=True)
    type = StringField(required=True)
    language = StringField(required=True)
    premiere_channel = ListField(EmbeddedDocumentField(PremiereChannel))
    streaming = ListField(EmbeddedDocumentField(Streaming))
    director = ListField(EmbeddedDocumentField(DirectorName))
    production = ListField(EmbeddedDocumentField(ProductionName))
    screenwriter = ListField(EmbeddedDocumentField(Screenwriter))
    starring = ListField(EmbeddedDocumentField(StarringId))
    image = URLField()
