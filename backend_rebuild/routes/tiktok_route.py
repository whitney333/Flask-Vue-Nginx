from flask import Blueprint, jsonify, request
from flask_restful import Resource, reqparse, Api
from controllers.sns.tiktok_controller import TiktokController

tiktok_bp = Blueprint('tiktok', __name__)
tiktok_api = Api(tiktok_bp)

# get tiktok followers
@tiktok_bp.route('/follower', methods=['GET'])
def get_tiktok_follower():
    artist_id = request.args.get('artist_id', type=str)
    date_end = request.args.get('date_end', type=str)
    filter = request.args.get('filter', type=str)

    followers = TiktokController.get_follower(artist_id, date_end, filter)

    return followers

# get tiktok likes
@tiktok_bp.route('/like', methods=['GET'])
def get_tiktok_like():
    artist_id = request.args.get('artist_id', type=str)
    date_end = request.args.get('date_end', type=str)
    filter = request.args.get('filter', type=str)

    likes = TiktokController.get_like(artist_id, date_end, filter)

    return likes

# get tiktok hashtags
@tiktok_bp.route('/hashtag', methods=['GET'])
def get_tiktok_hashtag():
    artist_id = request.args.get('artist_id', type=str)
    date_end = request.args.get('date_end', type=str)
    filter = request.args.get('filter', type=str)

    hashtags = TiktokController.get_hashtag(artist_id, date_end, filter)

    return hashtags
