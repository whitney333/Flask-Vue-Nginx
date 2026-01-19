from controllers.sns.instagram_controller import InstagramController
from flask import Blueprint, jsonify, request
from flask_restful import Api

instagram_bp = Blueprint('instagram', __name__)
instagram_api = Api(instagram_bp)

@instagram_bp.route('/v1/follower', methods=['GET'])
def get_instagram_follower():
    artist_id = request.args.get('artist_id', type=str)
    date_end = request.args.get('date_end', type=str)
    filter = request.args.get('filter', type=str)

    followers = InstagramController.get_follower(artist_id, date_end, filter)

    return followers

@instagram_bp.route('/v1/threads-follower', methods=['GET'])
def get_instagram_threads_follower():
    artist_id = request.args.get('artist_id', type=str)
    date_end = request.args.get('date_end', type=str)
    filter = request.args.get('filter', type=str)

    threads_followers = InstagramController.get_threads_follower(artist_id, date_end, filter)

    return threads_followers

@instagram_bp.route('/v1/post-count', methods=['GET'])
def get_instagram_post_count():
    artist_id = request.args.get('artist_id', type=str)
    date_end = request.args.get('date_end', type=str)
    filter = request.args.get('filter', type=str)

    post_count = InstagramController.get_post_count(artist_id, date_end, filter)

    return post_count

@instagram_bp.route('/v1/like', methods=['GET'])
def get_instagram_like():
    """
    Get Instagram latest 12 posts total likes & likes per post
    :return:
    """
    artist_id = request.args.get('artist_id', type=str)
    filter = request.args.get('filter', type=str)

    likes = InstagramController.get_likes(artist_id, filter)

    return likes

@instagram_bp.route('/v1/comment', methods=['GET'])
def get_instagram_comment():
    """
    Get Instagram latest 12 posts total comments & comments per post
    :return:
    """
    artist_id = request.args.get('artist_id', type=str)
    filter = request.args.get('filter', type=str)

    comments = InstagramController.get_comments(artist_id, filter)

    return comments

@instagram_bp.route('/v1/posts', methods=['GET'])
def get_instagram_latest_posts():
    """
    Get Instagram latest 12 posts information
    :return:
    """
    artist_id = request.args.get('artist_id', type=str)

    posts = InstagramController.get_instagram_latest_twelve_posts(artist_id)

    return posts

@instagram_bp.route('/v1/eng-rate/<string:artist_id>/<string:filter>', methods=['GET'])
def get_instagram_engagement_rate():
    pass

@instagram_bp.route('/v1/hashtag/most-used-five', methods=['GET'])
def get_most_used_recent_five_hashtags():
    artist_id = request.args.get('artist_id', type=str)
    most_used_hashtags = InstagramController.get_hashtags_most_used_recent_five(artist_id)

    return most_used_hashtags

@instagram_bp.route('/v1/hashtag/most-used-eight', methods=['GET'])
def get_most_used_recent_eight_hashtags():
    artist_id = request.args.get('artist_id', type=str)
    most_used_hashtags = InstagramController.get_hashtags_most_used_recent_eight(artist_id)

    return most_used_hashtags

@instagram_bp.route('/v1/hashtag/most-used-twelve', methods=['GET'])
def get_most_used_recent_twelve_hashtags():
    artist_id = request.args.get('artist_id', type=str)
    most_used_hashtags = InstagramController.get_hashtags_most_used_recent_twelve(artist_id)

    return most_used_hashtags

@instagram_bp.route('/v1/hashtag/most-engaged-five', methods=['GET'])
def get_most_engaged_recent_five_hashtags():
    artist_id = request.args.get('artist_id', type=str)
    most_engaged_hashtags = InstagramController.get_hashtags_most_engaged_recent_five(artist_id)

    return most_engaged_hashtags

@instagram_bp.route('/v1/hashtag/most-engaged-eight', methods=['GET'])
def get_most_engaged_recent_eight_hashtags():
    artist_id = request.args.get('artist_id', type=str)
    most_engaged_hashtags = InstagramController.get_hashtags_most_engaged_recent_eight(artist_id)

    return most_engaged_hashtags

@instagram_bp.route('/v1/hashtag/most-engaged-twelve', methods=['GET'])
def get_most_engaged_recent_twelve_hashtags():
    artist_id = request.args.get('artist_id', type=str)
    most_engaged_hashtags = InstagramController.get_hashtags_most_engaged_recent_twelve(artist_id)

    return most_engaged_hashtags

########################################################
# V2 endpoints
########################################################

@instagram_bp.route('/v2/chart/follower', methods=['GET'])
def get_instagram_follower_chart():
    artist_id = request.args.get('artist_id', type=str)
    date_end = request.args.get('date_end', type=str)
    days = request.args.get('days', type=int, default=7)

    followers = InstagramController.get_follower(artist_id, date_end, days)

    return followers

@instagram_bp.route('/v2/chart/threads-follower', methods=['GET'])
def get_instagram_threads_follower_chart():
    artist_id = request.args.get('artist_id', type=str)
    date_end = request.args.get('date_end', type=str)
    days = request.args.get('days', type=int, default=7)

    threads_followers = InstagramController.get_threads_follower(artist_id, date_end, days)

    return threads_followers

@instagram_bp.route('/v2/chart/post-count', methods=['GET'])
def get_instagram_post_count_chart():
    artist_id = request.args.get('artist_id', type=str)
    date_end = request.args.get('date_end', type=str)
    days = request.args.get('days', type=int, default=7)

    post_count = InstagramController.get_post_count(artist_id, date_end, days)

    return post_count

@instagram_bp.route('/v2/chart/like', methods=['GET'])
def get_instagram_like_chart():
    """
    Get Instagram latest posts total likes & likes per post
    :return:
    """
    artist_id = request.args.get('artist_id', type=str)
    date_end = request.args.get('date_end', type=str)
    days = request.args.get('days', type=int, default=7)

    likes = InstagramController.get_likes(artist_id, date_end, days)

    return likes

@instagram_bp.route('/v2/chart/comment', methods=['GET'])
def get_instagram_comment_chart():
    """
    Get Instagram latest posts total comments & comments per post
    :return:
    """
    artist_id = request.args.get('artist_id', type=str)
    date_end = request.args.get('date_end', type=str)
    days = request.args.get('days', type=int, default=7)

    comments = InstagramController.get_comments(artist_id, date_end, days)

    return comments

@instagram_bp.route('/v2/posts', methods=['GET'])
def get_instagram_latest_posts():
    """
    Get Instagram latest posts information
    :return:
    """
    artist_id = request.args.get('artist_id', type=str)
    posts_count = request.args.get('posts_count', type=int, default=12)

    posts = InstagramController.get_instagram_latest_posts(artist_id, posts_count)

    return posts

@instagram_bp.route('/v2/eng-rate/<string:artist_id>/<string:filter>', methods=['GET'])
def get_instagram_engagement_rate():
    pass

@instagram_bp.route('/v2/hashtag/most-used', methods=['GET'])
def get_most_used_hashtags():
    artist_id = request.args.get('artist_id', type=str)
    count = request.args.get('count', type=int, default=5)

    most_used_hashtags = InstagramController.get_hashtags_most_used(artist_id, count)

    return most_used_hashtags

@instagram_bp.route('/v2/hashtag/most-engaged', methods=['GET'])
def get_most_engaged_hashtags():
    artist_id = request.args.get('artist_id', type=str)
    count = request.args.get('count', type=int, default=5)

    most_engaged_hashtags = InstagramController.get_hashtags_most_engaged(artist_id, count)

    return most_engaged_hashtags
