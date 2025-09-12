from flask import Blueprint, jsonify, request
from flask_restful import Resource, reqparse, Api
from controllers.sns.bilibili_controller import BilibiliController


bilibili_bp = Blueprint('bilibili', __name__)
bilibili_api = Api(bilibili_bp)

@bilibili_bp.route('/v1/follower', methods=['GET'])
def get_bilibili_follower():
    artist_id = request.args.get('artist_id', type=str)
    date_end = request.args.get('date_end', type=str)
    filter = request.args.get('filter', type=str)

    follower = BilibiliController.get_follower(artist_id, date_end, filter)

    return follower

@bilibili_bp.route('/v1/view', methods=['GET'])
def get_bilibili_view():
    artist_id = request.args.get('artist_id', type=str)
    date_end = request.args.get('date_end', type=str)
    filter = request.args.get('filter', type=str)

    view = BilibiliController.get_view(artist_id, date_end, filter)

    return view

@bilibili_bp.route('/v1/like', methods=['GET'])
def get_bilibili_like():
    artist_id = request.args.get('artist_id', type=str)
    date_end = request.args.get('date_end', type=str)
    filter = request.args.get('filter', type=str)

    like = BilibiliController.get_like(artist_id, date_end, filter)

    return like

@bilibili_bp.route('/v1/comment', methods=['GET'])
def get_bilibili_comment():
    artist_id = request.args.get('artist_id', type=str)
    date_end = request.args.get('date_end', type=str)
    filter = request.args.get('filter', type=str)

    comment = BilibiliController.get_comment(artist_id, date_end, filter)

    return comment

@bilibili_bp.route('/v1/share', methods=['GET'])
def get_bilibili_share():
    artist_id = request.args.get('artist_id', type=str)
    date_end = request.args.get('date_end', type=str)
    filter = request.args.get('filter', type=str)

    share = BilibiliController.get_share(artist_id, date_end, filter)

    return share

@bilibili_bp.route('/v1/coin', methods=['GET'])
def get_bilibili_coin():
    artist_id = request.args.get('artist_id', type=str)
    date_end = request.args.get('date_end', type=str)
    filter = request.args.get('filter', type=str)

    coin = BilibiliController.get_coin(artist_id, date_end, filter)

    return coin

@bilibili_bp.route('/v1/collect', methods=['GET'])
def get_bilibili_collect():
    artist_id = request.args.get('artist_id', type=str)
    date_end = request.args.get('date_end', type=str)
    filter = request.args.get('filter', type=str)

    collect = BilibiliController.get_collect(artist_id, date_end, filter)

    return collect

@bilibili_bp.route('/v1/danmu', methods=['GET'])
def get_bilibili_danmu():
    artist_id = request.args.get('artist_id', type=str)
    date_end = request.args.get('date_end', type=str)
    filter = request.args.get('filter', type=str)

    danmu = BilibiliController.get_bullet_chat(artist_id, date_end, filter)

    return danmu

@bilibili_bp.route('/v1/engagement-rate', methods=['GET'])
def get_bilibili_engagement_rate():
    artist_id = request.args.get('artist_id', type=str)
    date_end = request.args.get('date_end', type=str)
    filter = request.args.get('filter', type=str)

    engagement_rate = BilibiliController.get_engagement_rate(artist_id, date_end, filter)

    return engagement_rate

@bilibili_bp.route('/v1/posts', methods=['GET'])
def get_bilibili_latest_posts():
    artist_id = request.args.get('artist_id', type=str)

    posts = BilibiliController.get_latest_thirty_posts(artist_id)

    return posts
