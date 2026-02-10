from flask import Blueprint, jsonify, request
from flask_restful import Resource, reqparse, Api
from controllers.sns.bilibili_controller import BilibiliController


bilibili_bp = Blueprint('bilibili', __name__)
bilibili_api = Api(bilibili_bp)


@bilibili_bp.route('/v1/follower/growth', methods=['GET'])
def get_bilibili_follower_growth():
    artist_id = request.args.get('artist_id', type=str)
    campaign_start = request.args.get('start', type=str)

    return BilibiliController.get_bilibili_follower_growth(artist_id, campaign_start)

@bilibili_bp.route('/v1/follower', methods=['GET'])
def get_bilibili_follower():
    artist_id = request.args.get("artist_id")
    date_end = request.args.get("date_end")
    range_key = request.args.get("range")

    result = BilibiliController.get_bilibili_follower(
        artist_id=artist_id,
        date_end=date_end,
        range=range_key
    )

    return result

@bilibili_bp.route('/v1/view', methods=['GET'])
def get_bilibili_view():
    artist_id = request.args.get("artist_id")
    date_end = request.args.get("date_end")
    range_key = request.args.get("range")

    result = BilibiliController.get_bilibili_views(
        artist_id=artist_id,
        date_end=date_end,
        range=range_key
    )

    return result

@bilibili_bp.route('/v1/like', methods=['GET'])
def get_bilibili_like():
    artist_id = request.args.get("artist_id")
    date_end = request.args.get("date_end")
    range_key = request.args.get("range")

    result = BilibiliController.get_bilibili_likes(
        artist_id=artist_id,
        date_end=date_end,
        range=range_key
    )

    return result

@bilibili_bp.route('/v1/comment', methods=['GET'])
def get_bilibili_comment():
    artist_id = request.args.get("artist_id")
    date_end = request.args.get("date_end")
    range_key = request.args.get("range")

    result = BilibiliController.get_bilibili_comments(
        artist_id=artist_id,
        date_end=date_end,
        range=range_key
    )

    return result

@bilibili_bp.route('/v1/share', methods=['GET'])
def get_bilibili_share():
    artist_id = request.args.get("artist_id")
    date_end = request.args.get("date_end")
    range_key = request.args.get("range")

    result = BilibiliController.get_bilibili_shares(
        artist_id=artist_id,
        date_end=date_end,
        range=range_key
    )

    return result

@bilibili_bp.route('/v1/coin', methods=['GET'])
def get_bilibili_coin():
    artist_id = request.args.get("artist_id")
    date_end = request.args.get("date_end")
    range_key = request.args.get("range")

    result = BilibiliController.get_bilibili_coins(
        artist_id=artist_id,
        date_end=date_end,
        range=range_key
    )

    return result

@bilibili_bp.route('/v1/collect', methods=['GET'])
def get_bilibili_collect():
    artist_id = request.args.get("artist_id")
    date_end = request.args.get("date_end")
    range_key = request.args.get("range")

    result = BilibiliController.get_bilibili_collects(
        artist_id=artist_id,
        date_end=date_end,
        range=range_key
    )

    return result

@bilibili_bp.route('/v1/danmu', methods=['GET'])
def get_bilibili_danmu():
    artist_id = request.args.get("artist_id")
    date_end = request.args.get("date_end")
    range_key = request.args.get("range")

    result = BilibiliController.get_bilibili_danmus(
        artist_id=artist_id,
        date_end=date_end,
        range=range_key
    )

    return result

@bilibili_bp.route('/v1/engagement-rate', methods=['GET'])
def get_bilibili_engagement_rate():
    artist_id = request.args.get("artist_id")
    date_end = request.args.get("date_end")
    range_key = request.args.get("range")

    result = BilibiliController.get_bilibili_engagement(
        artist_id=artist_id,
        date_end=date_end,
        range=range_key
    )

    return result

@bilibili_bp.route('/v1/posts', methods=['GET'])
def get_bilibili_latest_posts():
    artist_id = request.args.get('artist_id', type=str)

    result = BilibiliController.get_bilibili_latest_videos(
        artist_id=artist_id
    )

    return result
