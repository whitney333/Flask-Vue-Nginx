from flask import Blueprint, jsonify, request
from flask_restful import Resource, reqparse, Api
from controllers.artist_controller import ArtistController

artist_bp = Blueprint('artist', __name__)
artist_api = Api(artist_bp)

@artist_bp.route("/v1/artist", methods=["POST"])
def create_artist():
    return ArtistController.create_artist()

@artist_bp.route("/v1/artist/<string:artist_id>", methods=["GET"])
def get_artist_by_id(artist_id):
    return ArtistController.get_artist_by_id(artist_id)

@artist_bp.route("/v1/artist/tenant/<string:tenant_id>", methods=["GET"])
def get_artists_by_tenant_id(tenant_id):
    return ArtistController.get_artists_by_tenant_id(tenant_id)

@artist_bp.route("/v1/artist/all", methods=["GET"])
def get_all_artists():
    return ArtistController.get_all_artists()

