from flask import Blueprint, jsonify, request
from flask_restful import Resource, reqparse, Api
from controllers.artist_controller import ArtistsController
from libs.utils import auth_required


artist_bp = Blueprint("artist", __name__)
artist_api = Api(artist_bp)

@artist_bp.route("/v1/artist", methods=["POST"])
def create_artist():
    return ArtistsController.create_artist()

@artist_bp.route("/v1/artist/<string:artist_id>", methods=["GET"])
def get_artist_by_id(artist_id):
    return ArtistsController.get_artist_by_id(artist_id)

@artist_bp.route("/v1/artist/all", methods=["GET"])
def get_all_artist():
    return ArtistsController.get_all_artists()

@artist_bp.route("/info", methods=["GET"])
def get_artist_info():
    artist_id = request.args.get("artist_id", type=str)

    result = ArtistsController.new_get_artist_info(artist_id)

    return result
