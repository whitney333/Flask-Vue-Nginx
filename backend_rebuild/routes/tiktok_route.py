from flask import Blueprint, jsonify, request
from flask_restful import Resource, reqparse, Api
from controllers.sns.tiktok_controller import TiktokController

tiktok_bp = Blueprint('tiktok', __name__)
tiktok_api = Api(tiktok_bp)

# get tiktok followers
@tiktok_bp.route('/follower/<string:artist_id>/<string:date_end>/<string:filter>', methods=['GET'])
def get_tiktok_follower(artist_id, date_end, filter):
    try:
        followers = TiktokController.get_follower(artist_id, date_end, filter)
        return jsonify(followers), 200
    except Exception as e:
        return jsonify({'err': str(e)}), 500

# get tiktok likes
@tiktok_bp.route('/follower/<string:artist_id>/<string:date_end>/<string:filter>', methods=['GET'])
def get_tiktok_like(artist_id, date_end, filter):
    try:
        likes = TiktokController.get_like(artist_id, date_end, filter)
        return jsonify(likes), 200
    except Exception as e:
        return jsonify({'err': str(e)}), 500

# get tiktok hashtags
@tiktok_bp.route('/follower/<string:artist_id>/<string:date_end>/<string:filter>', methods=['GET'])
def get_tiktok_hashtag(artist_id, date_end, filter):
    try:
        hashtags = TiktokController.get_hashtag(artist_id, date_end, filter)
        return jsonify(hashtags), 200
    except Exception as e:
        return jsonify({'err': str(e)}), 500


