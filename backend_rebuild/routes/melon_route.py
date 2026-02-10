from flask import Blueprint, jsonify, request
from flask_restful import Resource, reqparse, Api
from controllers.melon_controller import MelonController
from libs.utils import auth_required

melon_bp = Blueprint('melon', __name__)
melon_api = Api(melon_bp)

@melon_bp.route('/v1/follower', methods=['GET'])
def get_melon_follower():
    artist_id = request.args.get("artist_id")
    date_end = request.args.get("date_end")
    range_key = request.args.get("range")

    result = MelonController.get_melon_follower(
        artist_id=artist_id,
        date_end=date_end,
        range=range_key
    )

    return result

@melon_bp.route("/v2/follower/<string:artist_id>", methods=["GET"])
@auth_required
def get_melon_follower_by_artist_id(artist_id):
    result = MelonController.get_melon_follower_by_artist_id(artist_id)

    return result
