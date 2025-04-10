from controllers.sns.instagram_controller import InstagramController
from flask import Blueprint, jsonify, request
from flask_restful import Api

instagram_bp = Blueprint('instagram', __name__)
instagram_api = Api(instagram_bp)

@instagram_bp.route('/instagram/follower/<string:artist_id>/<string:date_end>/<string:filter>', methods=['GET'])
def get_instagram_follower(artist_id, date_end, filter):
    try:
        followers = InstagramController.get_follower(artist_id, date_end, filter)
        return jsonify(followers), 200
    except Exception as e:
        return jsonify({'err': str(e)}), 500


@instagram_bp.route('/instagram/threads-follower/<string:artist_id>/<string:date_end>/<string:filter>', methods=['GET'])
def get_instagram_threads_follower(artist_id, date_end, filter):
    try:
        threads_followers = InstagramController.get_threads_follower(artist_id, date_end, filter)
        return jsonify(threads_followers), 200
    except Exception as e:
        return jsonify({'err': str(e)}), 500

@instagram_bp.route('/instagram/post-count/<string:artist_id>/<string:date_end>/<string:filter>', methods=['GET'])
def get_instagram_post_count(artist_id, date_end, filter):
    try:
        post_count = InstagramController.get_post_count(artist_id, date_end, filter)
        return jsonify(post_count), 200
    except Exception as e:
        return jsonify({'err': str(e)}), 500


@instagram_bp.route('/instagram/like/<string:artist_id>/<string:filter>', methods=['GET'])
def get_instagram_like(artist_id, filter):
    """
    Get Instagram latest 12 posts total likes & likes per post
    :return:
    """
    try:
        likes = InstagramController.get_likes(artist_id, filter)
        return jsonify(likes), 200
    except Exception as e:
        return jsonify({'err': str(e)}), 500

@instagram_bp.route('/instagram/comment/<string:artist_id>/<string:filter>', methods=['GET'])
def get_instagram_comment(artist_id, filter):
    """
    Get Instagram latest 12 posts total comments & comments per post
    :return:
    """
    try:
        comments = InstagramController.get_comments(artist_id, filter)
        return jsonify(comments), 200
    except Exception as e:
        return jsonify({'err': str(e)}), 500

@instagram_bp.route()
def get_instagram_engagement_rate():
    pass

