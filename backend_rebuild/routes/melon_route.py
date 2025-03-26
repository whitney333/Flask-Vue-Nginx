from flask import Blueprint, jsonify, request
from flask_restful import Resource, reqparse, Api
from backend_rebuild.controllers.melon_controller import MelonController

melon_bp = Blueprint('melon', __name__)
melon_api = Api(melon_bp)

@melon_bp.route('/melon/follower/<int:artist_id>/<string:date_end>/<string:filter>', methods=['GET'])
def get_melon_follower(artist_id, date_end, filter):
    try:
        follower = MelonController.get_follower(artist_id, date_end, filter)
        return jsonify(follower), 200
    except Exception as e:
        return jsonify({'err': str(e)}), 500
