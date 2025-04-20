from flask import Blueprint, jsonify, request
from flask_restful import Resource, reqparse, Api
from controllers.sns.youtube_controller import YoutubeController

youtube_bp = Blueprint('youtube', __name__)
youtube_api = Api(youtube_bp)

# get youtube subscribers
@youtube_bp.route('/follower', methods=['GET'])
def get_youtube_subscriber():
    artist_id = request.args.get('artist_id', type=str)
    date_end = request.args.get('date_end', type=str)
    filter = request.args.get('filter', type=str)

    subscribers = YoutubeController.get_subscribers(artist_id, date_end, filter)

    return subscribers

# get youtube channel views
@youtube_bp.route('/channel-view', methods=['GET'])
def get_youtube_channel_view():
    artist_id = request.args.get('artist_id', type=str)
    date_end = request.args.get('date_end', type=str)
    filter = request.args.get('filter', type=str)

    channel_view = YoutubeController.get_youtube_channel_view(artist_id, date_end, filter)

    return channel_view

# get youtube channel hashtag counts
@youtube_bp.route('/channel-hashtag', methods=['GET'])
def get_youtube_channel_hashtag():
    artist_id = request.args.get('artist_id', type=str)
    date_end = request.args.get('date_end', type=str)
    filter = request.args.get('filter', type=str)

    channel_hashtag = YoutubeController.get_youtube_channel_hashtag(artist_id, date_end, filter)

    return channel_hashtag

# get youtube video hashtag counts
@youtube_bp.route('/video-hashtag', methods=['GET'])
def get_youtube_video_hashtag():
    artist_id = request.args.get('artist_id', type=str)
    date_end = request.args.get('date_end', type=str)
    filter = request.args.get('filter', type=str)

    video_hashtag = YoutubeController.get_youtube_video_hashtag(artist_id, date_end, filter)

    return video_hashtag

# get youtube latest 50 videos indexes
@youtube_bp.route('/video-index', methods=['GET'])
def get_youtube_video_index():
    artist_id = request.args.get('artist_id', type=str)
    filter = request.args.get('filter', type=str)

    video_index = YoutubeController.get_youtube_video_index(artist_id, filter)

    return video_index

