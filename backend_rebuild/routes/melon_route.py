from flask import Blueprint, jsonify, request
from flask_restful import Resource, reqparse, Api
from controllers.melon_controller import MelonController

melon_bp = Blueprint('melon', __name__)
melon_api = Api(melon_bp)

@melon_bp.route('/v1/follower', methods=['GET'])
def get_melon_follower():
    artist_id = request.args.get('artist_id', type=str)
    date_end = request.args.get('date_end', type=str)
    filter = request.args.get('filter', type=str)

    follower = MelonController.get_follower(artist_id, date_end, filter)

    return follower

@melon_bp.route("/v2/follower/<string:artist_id>", methods=["GET"])
def get_melon_follower_by_artist_id(artist_id):
    result = MelonController.get_melon_follower_by_artist_id(artist_id)

    return result
