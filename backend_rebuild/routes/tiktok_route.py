from flask import Blueprint, jsonify, request
from flask_restful import Resource, reqparse, Api
from controllers.sns.tiktok_controller import TiktokController

tiktok_bp = Blueprint('tiktok', __name__)
tiktok_api = Api(tiktok_bp)

# get tiktok followers
@tiktok_bp.route('/v1/follower', methods=['GET'])
def get_tiktok_follower():
    artist_id = request.args.get("artist_id")
    date_end = request.args.get("date_end")
    range_key = request.args.get("range")

    result = TiktokController.get_tiktok_follower(
        artist_id=artist_id,
        date_end=date_end,
        range=range_key
    )

    return result

# get tiktok likes
@tiktok_bp.route('/v1/like', methods=['GET'])
def get_tiktok_like():
    artist_id = request.args.get("artist_id")
    date_end = request.args.get("date_end")
    range_key = request.args.get("range")

    result = TiktokController.get_tiktok_likes(
        artist_id=artist_id,
        date_end=date_end,
        range=range_key
    )

    return result

# get tiktok hashtags
@tiktok_bp.route('/v1/hashtag', methods=['GET'])
def get_tiktok_hashtag():
    artist_id = request.args.get("artist_id")
    date_end = request.args.get("date_end")
    range_key = request.args.get("range")

    result = TiktokController.get_tiktok_hashtags(
        artist_id=artist_id,
        date_end=date_end,
        range=range_key
    )

    return result

@tiktok_bp.route("/v1/follower/growth", methods=["GET"])
def get_tiktok_follower_growth():
    artist_id = request.args.get('artist_id', type=str)
    campaign_start = request.args.get('start', type=str)

    result = TiktokController.get_tiktok_follower_growth(artist_id, campaign_start)

    return result

@tiktok_bp.route("/v1/hashtag/growth", methods=["GET"])
def get_tiktok_hashtag_growth():
    artist_id = request.args.get('artist_id', type=str)
    campaign_start = request.args.get('start', type=str)

    result = TiktokController.get_tiktok_hashtag_growth(artist_id, campaign_start)

    return result
