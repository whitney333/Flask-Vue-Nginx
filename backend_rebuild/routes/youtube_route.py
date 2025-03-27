from flask import Blueprint, jsonify, request
from flask_restful import Resource, reqparse, Api
from controllers.sns.youtube_controller import YoutubeController

youtube_bp = Blueprint('youtube', __name__)
youtube_api = Api(youtube_bp)

# get youtube subscribers
@youtube_bp.route('/youtube/follower/<string:artist_id>/<string:date_end>/<string:filter>', methods=['GET'])
def get_youtube_subscriber(artist_id, date_end, filter):
    try:
        subscribers = YoutubeController.get_subscribers(artist_id, date_end, filter)
        return jsonify(subscribers), 200
    except Exception as e:
        return jsonify({'err': str(e)}), 500

# get youtube channel views
@youtube_bp.route('/youtube/channel-view/<string:artist_id>/<string:date_end>/<string:filter>', methods=['GET'])
def get_youtube_channel_view(artist_id, date_end, filter):
    try:
        channel_view = YoutubeController.get_youtube_channel_view(artist_id, date_end, filter)
        return jsonify(channel_view), 200
    except Exception as e:
        return jsonify({'err': str(e)}), 500

# get youtube channel hashtag counts
@youtube_bp.route('/youtube/channel-hashtag/<string:artist_id>/<string:date_end>/<string:filter>', methods=['GET'])
def get_youtube_channel_hashtag(artist_id, date_end, filter):
    try:
        channel_hashtag = YoutubeController.get_youtube_channel_hashtag(artist_id, date_end, filter)
        return jsonify(channel_hashtag), 200
    except Exception as e:
        return jsonify({'err': str(e)}), 500

# get youtube video hashtag counts
@youtube_bp.route('/youtube/video-hashtag/<string:artist_id>/<string:date_end>/<string:filter>', methods=['GET'])
def get_youtube_video_hashtag(artist_id, date_end, filter):
    try:
        video_hashtag = YoutubeController.get_youtube_channel_hashtag(artist_id, date_end, filter)
        return jsonify(video_hashtag), 200
    except Exception as e:
        return jsonify({'err': str(e)}), 500

# get youtube latest 50 videos indexes
@youtube_bp.route('/youtube/video-index/<string:artist_id>/<string:filter>', methods=['GET'])
def get_youtube_video_index(artist_id, filter):
    try:
        video_index = YoutubeController.get_youtube_video_index(artist_id, filter)
        return jsonify(video_index), 200
    except Exception as e:
        return jsonify({'err': str(e)}), 500

