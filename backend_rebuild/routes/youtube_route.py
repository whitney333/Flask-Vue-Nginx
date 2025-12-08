from flask import Blueprint, jsonify, request
from flask_restful import Resource, reqparse, Api
from controllers.sns.youtube_controller import YoutubeController
from libs.utils import auth_required

youtube_bp = Blueprint('youtube', __name__)
youtube_api = Api(youtube_bp)


# ARCHIVE
# get youtube subscribers
# @youtube_bp.route('/v1/follower', methods=['GET'])
# def get_youtube_subscriber():
#     artist_id = request.args.get('artist_id', type=str)
#     date_end = request.args.get('date_end', type=str)
#     filter = request.args.get('filter', type=str)
#
#     subscribers = YoutubeController.get_subscribers(artist_id, date_end, filter)
#
#     return subscribers

# ARCHIVE
# get youtube channel views
@youtube_bp.route('/v1/channel-view', methods=['GET'])
def get_youtube_channel_view():
    artist_id = request.args.get('artist_id', type=str)
    date_end = request.args.get('date_end', type=str)
    filter = request.args.get('filter', type=str)

    channel_view = YoutubeController.get_youtube_channel_view(artist_id, date_end, filter)

    return channel_view

# get youtube latest 12 videos total views
@youtube_bp.route('/v1/video-view', methods=['GET'])
def get_youtube_video_view():
    artist_id = request.args.get('artist_id', type=str)
    date_end = request.args.get('date_end', type=str)
    filter = request.args.get('filter', type=str)

    video_view = YoutubeController.get_youtube_video_view(artist_id, date_end, filter)

    return video_view

# ARCHIVE
# get youtube channel hashtag counts
@youtube_bp.route('/channel-hashtag', methods=['GET'])
def get_youtube_channel_hashtag():
    artist_id = request.args.get('artist_id', type=str)
    date_end = request.args.get('date_end', type=str)
    filter = request.args.get('filter', type=str)

    channel_hashtag = YoutubeController.get_youtube_channel_hashtag(artist_id, date_end, filter)

    return channel_hashtag

# ARCHIVE
# get youtube video hashtag counts
@youtube_bp.route('/video-hashtag', methods=['GET'])
def get_youtube_video_hashtag():
    artist_id = request.args.get('artist_id', type=str)
    date_end = request.args.get('date_end', type=str)
    filter = request.args.get('filter', type=str)

    video_hashtag = YoutubeController.get_youtube_video_hashtag(artist_id, date_end, filter)

    return video_hashtag

# get youtube channel basic info
@youtube_bp.route('/v1/channel', methods=['GET'])
def get_youtube_channel_basic_info():
    artist_id = request.args.get('artist_id', type=str)
    date_end = request.args.get('date_end', type=str)
    filter = request.args.get('filter', type=str)

    result = YoutubeController.get_channel_basic(artist_id, date_end, filter)

    return result

# get youtube latest 50 videos indexes
@youtube_bp.route('/v1/video-index', methods=['GET'])
def get_youtube_video_index():
    artist_id = request.args.get('artist_id', type=str)
    filter = request.args.get('filter', type=str)

    video_index = YoutubeController.get_youtube_video_index(artist_id, filter)

    return video_index

# get youtube latest videos information
@youtube_bp.route('/v1/posts', methods=['GET'])
def get_youtube_videos():
    artist_id = request.args.get('artist_id', type=str)

    videos = YoutubeController.get_youtube_latest_video_info(artist_id)

    return videos

# get youtube most-used hashtags in recent 5 posts
@youtube_bp.route('/v1/hashtag/most-used-five', methods=['GET'])
def get_most_used_recent_five_hashtags():
    artist_id = request.args.get('artist_id', type=str)

    hashtags = YoutubeController.get_hashtags_most_used_recent_five(artist_id)

    return hashtags

# get youtube most-used hashtags in recent 8 posts
@youtube_bp.route('/v1/hashtag/most-used-eight', methods=['GET'])
def get_most_used_recent_eight_hashtags():
    artist_id = request.args.get('artist_id', type=str)

    hashtags = YoutubeController.get_hashtags_most_used_recent_eight(artist_id)

    return hashtags

# get youtube most-used hashtags in recent 12 posts
@youtube_bp.route('/v1/hashtag/most-used-twelve', methods=['GET'])
def get_most_used_recent_twelve_hashtags():
    artist_id = request.args.get('artist_id', type=str)

    hashtags = YoutubeController.get_hashtags_most_used_recent_twelve(artist_id)

    return hashtags

# get youtube most-engaged hashtags in recent 5 posts
@youtube_bp.route('/v1/hashtag/most-engaged-five', methods=['GET'])
def get_most_engaged_recent_five_hashtags():
    artist_id = request.args.get('artist_id', type=str)

    hashtags = YoutubeController.get_hashtags_most_engaged_recent_five(artist_id)

    return hashtags

# get youtube most-engaged hashtags in recent 8 posts
@youtube_bp.route('/v1/hashtag/most-engaged-eight', methods=['GET'])
def get_most_engaged_recent_eight_hashtags():
    artist_id = request.args.get('artist_id', type=str)

    hashtags = YoutubeController.get_hashtags_most_engaged_recent_eight(artist_id)

    return hashtags

# get youtube most-engaged hashtags in recent 12 posts
@youtube_bp.route('/v1/hashtag/most-engaged-twelve', methods=['GET'])
def get_most_engaged_recent_twelve_hashtags():
    artist_id = request.args.get('artist_id', type=str)

    hashtags = YoutubeController.get_hashtags_most_engaged_recent_twelve(artist_id)

    return hashtags

#################### v2 Endpoint ####################
@youtube_bp.route("/v2/channel/<string:artist_id>", methods=['GET'])
@auth_required
def get_youtube_channel_basic_by_artist_id(artist_id):
    result = YoutubeController.get_youtube_channel_basic_by_artist_id(artist_id)

    return result

@youtube_bp.route("/v2/video-index/<string:artist_id>", methods=['GET'])
@auth_required
def get_youtube_video_index_by_artist_id(artist_id):
    result = YoutubeController.get_youtube_video_index_by_artist_id(artist_id)

    return result

@youtube_bp.route("/v2/channel-view/<string:artist_id>", methods=['GET'])
@auth_required
def get_youtube_channel_view_by_artist_id(artist_id):
    result = YoutubeController.get_youtube_channel_view_by_artist_id(artist_id)

    return result

@youtube_bp.route("/v2/video-view/<string:artist_id>", methods=['GET'])
@auth_required
def get_youtube_video_view_by_artist_id(artist_id):
    result = YoutubeController.get_youtube_video_view_by_artist_id(artist_id)

    return result

@youtube_bp.route("/v2/posts/<string:artist_id>", methods=['GET'])
@auth_required
def get_youtube_latest_video_info(artist_id):
    result = YoutubeController.get_youtube_latest_video_info_by_artist_id(artist_id)

    return result

@youtube_bp.route("/v2/hashtag/most-used-five/<string:artist_id>", methods=['GET'])
@auth_required
def get_youtube_most_used_five_hashtag_by_artist_id(artist_id):
    result = YoutubeController.get_hashtags_most_used_recent_five_by_artist_id(artist_id)

    return result

@youtube_bp.route("/v2/hashtag/most-used-eight/<string:artist_id>", methods=['GET'])
@auth_required
def get_youtube_most_used_eight_hashtag_by_artist_id(artist_id):
    result = YoutubeController.get_hashtags_most_used_recent_eight_by_artist_id(artist_id)

    return result

@youtube_bp.route("/v2/hashtag/most-used-twelve/<string:artist_id>", methods=['GET'])
@auth_required
def get_youtube_most_used_twelve_hashtag_by_artist_id(artist_id):
    result = YoutubeController.get_hashtags_most_used_recent_twelve_by_artist_id(artist_id)

    return result

@youtube_bp.route("/v2/hashtag/most-engaged-five/<string:artist_id>", methods=['GET'])
@auth_required
def get_youtube_most_engaged_five_hashtag_by_artist_id(artist_id):
    result = YoutubeController.get_hashtags_most_engaged_recent_five_by_artist_id(artist_id)

    return result

@youtube_bp.route("/v2/hashtag/most-engaged-eight/<string:artist_id>", methods=['GET'])
@auth_required
def get_youtube_most_engaged_eight_hashtag_by_artist_id(artist_id):
    result = YoutubeController.get_hashtags_most_engaged_recent_five_by_artist_id(artist_id)

    return result

@youtube_bp.route("/v2/hashtag/most-engaged-twelve/<string:artist_id>", methods=['GET'])
@auth_required
def get_youtube_most_engaged_twelve_hashtag_by_artist_id(artist_id):
    result = YoutubeController.get_hashtags_most_engaged_recent_twelve_by_artist_id(artist_id)

    return result
