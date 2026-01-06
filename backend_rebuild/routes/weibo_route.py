from flask import Blueprint, jsonify, request
from flask_restful import Resource, reqparse, Api
from controllers.sns.weibo_controller import WeiboController


weibo_bp = Blueprint('weibo', __name__)
weibo_api = Api(weibo_bp)

@weibo_bp.route('/v1/follower/growth', methods=['GET'])
def get_weibo_follower_growth():
    artist_id = request.args.get('artist_id', type=str)
    campaign_start = request.args.get('start', type=str)

    return WeiboController.get_weibo_follower_growth(artist_id, campaign_start)

@weibo_bp.route('/v1/follower/growth', methods=['GET'])
def get_weibo_follower_growth():
    artist_id = request.args.get('artist_id', type=str)
    campaign_start = request.args.get('start', type=str)

    return WeiboController.get_weibo_follower_growth(artist_id, campaign_start)

@weibo_bp.route('/v1/like/growth', methods=['GET'])
def get_weibo_like_growth():
    artist_id = request.args.get('artist_id', type=str)
    campaign_start = request.args.get('start', type=str)

    return WeiboController.get_weibo_like_growth(artist_id, campaign_start)

@weibo_bp.route('/v1/share/growth', methods=['GET'])
def get_weibo_share_growth():
    artist_id = request.args.get('artist_id', type=str)
    campaign_start = request.args.get('start', type=str)

    return WeiboController.get_weibo_share_growth(artist_id, campaign_start)

@weibo_bp.route('/v1/engagement/growth', methods=['GET'])
def get_weibo_engagement_growth():
    artist_id = request.args.get('artist_id', type=str)
    campaign_start = request.args.get('start', type=str)

    return WeiboController.get_weibo_engagement_growth(artist_id, campaign_start)
