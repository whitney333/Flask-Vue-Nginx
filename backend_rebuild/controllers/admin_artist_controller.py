from models.tenant_model import Tenant
from models.user_model import Users
from models.artist_model import Artists
from flask import jsonify, request
from datetime import datetime, timezone
from firebase_admin import auth


class AdminArtistController:
    def __init__(self, admin):
        self.admin = admin

    @classmethod
    def getAllArtists(cls):
        pass

    @classmethod
    def getSingleArtist(cls):
        pass

    @classmethod
    def addArtist(cls):
        pass

    @classmethod
    def updateArtist(cls):
        pass

    @classmethod
    def cancelArtist(cls):
        pass
