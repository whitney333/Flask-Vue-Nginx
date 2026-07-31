from flask import Blueprint, jsonify, request
from flask_restful import Resource, reqparse, Api
from controllers.sns.weibo_controller import WeiboController
from libs.utils import auth_required


weibo_bp = Blueprint('weibo', __name__)
weibo_api = Api(weibo_bp)

@weibo_bp.route('/v1/follower/growth', methods=['GET'])
@auth_required
def get_weibo_follower_growth():
    artist_id = request.args.get('artist_id', type=str)
    campaign_start = request.args.get('start', type=str)

    return WeiboController.get_weibo_follower_growth(artist_id, campaign_start)

@weibo_bp.route('/v1/like/growth', methods=['GET'])
@auth_required
def get_weibo_like_growth():
    artist_id = request.args.get('artist_id', type=str)
    campaign_start = request.args.get('start', type=str)

    return WeiboController.get_weibo_like_growth(artist_id, campaign_start)

@weibo_bp.route('/v1/share/growth', methods=['GET'])
@auth_required
def get_weibo_share_growth():
    artist_id = request.args.get('artist_id', type=str)
    campaign_start = request.args.get('start', type=str)

    return WeiboController.get_weibo_share_growth(artist_id, campaign_start)

@weibo_bp.route('/v1/engagement/growth', methods=['GET'])
@auth_required
def get_weibo_engagement_growth():
    artist_id = request.args.get('artist_id', type=str)
    campaign_start = request.args.get('start', type=str)

    return WeiboController.get_weibo_engagement_growth(artist_id, campaign_start)

@weibo_bp.route('/v1/follower', methods=['GET'])
@auth_required
def get_weibo_follower():
    artist_id = request.args.get("artist_id")
    date_end = request.args.get("date_end")
    range_key = request.args.get("range")

    result = WeiboController.get_weibo_follower(
        artist_id=artist_id,
        date_end=date_end,
        range=range_key
    )

    return result

@weibo_bp.route('/v1/status', methods=['GET'])
@auth_required
def get_weibo_status():
    artist_id = request.args.get("artist_id")
    date_end = request.args.get("date_end")
    range_key = request.args.get("range")

    result = WeiboController.get_weibo_status(
        artist_id=artist_id,
        date_end=date_end,
        range=range_key
    )

    return result

@weibo_bp.route('/v1/like', methods=['GET'])
@auth_required
def get_weibo_like():
    artist_id = request.args.get("artist_id")
    date_end = request.args.get("date_end")
    range_key = request.args.get("range")

    result = WeiboController.get_weibo_like(
        artist_id=artist_id,
        date_end=date_end,
        range=range_key
    )

    return result

@weibo_bp.route('/v1/comment', methods=['GET'])
@auth_required
def get_weibo_comment():
    artist_id = request.args.get("artist_id")
    date_end = request.args.get("date_end")
    range_key = request.args.get("range")

    result = WeiboController.get_weibo_comment(
        artist_id=artist_id,
        date_end=date_end,
        range=range_key
    )

    return result

@weibo_bp.route('/v1/share', methods=['GET'])
@auth_required
def get_weibo_share():
    artist_id = request.args.get("artist_id")
    date_end = request.args.get("date_end")
    range_key = request.args.get("range")

    result = WeiboController.get_weibo_share(
        artist_id=artist_id,
        date_end=date_end,
        range=range_key
    )

    return result

@weibo_bp.route('/v1/engagement', methods=['GET'])
@auth_required
def get_weibo_engagement():
    artist_id = request.args.get("artist_id")
    date_end = request.args.get("date_end")
    range_key = request.args.get("range")

    result = WeiboController.get_weibo_engagement(
        artist_id=artist_id,
        date_end=date_end,
        range=range_key
    )

    return result
