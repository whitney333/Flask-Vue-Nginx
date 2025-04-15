from flask import Blueprint, jsonify, request
from flask_restful import Resource, reqparse, Api
from controllers.spotify_controller import SpotifyController

spotify_bp = Blueprint('spotify', __name__)
spotify_api = Api(spotify_bp)

# spotify follower route
@spotify_bp.route('/follower/<string:artist_id>/<string:date_end>/<string:filter>', methods=['GET'])
def get_spotify_follower(artist_id, date_end, filter):
    try:
        follower = SpotifyController.get_follower(artist_id, date_end, filter)
        return jsonify(follower), 200
    except Exception as e:
        return jsonify({'err': str(e)}), 500

# spotify monthly_listener route
@spotify_bp.route('/monthly_listener/<string:artist_id>/<string:date_end>/<string:filter>', methods=['GET'])
def get_spotify_monthly_listener(artist_id, date_end, filter):
    try:
        listener = SpotifyController.get_monthly_listener(artist_id, date_end, filter)
        return jsonify(listener), 200
    except Exception as e:
        return jsonify({'err': str(e)}), 500

# spotify popularity route
@spotify_bp.route('/popularity/<string:artist_id>/<string:date_end>/<string:filter>', methods=['GET'])
def get_spotify_popularity(artist_id, date_end, filter):
    try:
        popularity = SpotifyController.get_popularity(artist_id, date_end, filter)
        return jsonify(popularity), 200
    except Exception as e:
        return jsonify({'err': str(e)}), 500

# spotify fan conversion rate route
@spotify_bp.route('/conversion_rate/<string:artist_id>/<string:date_end>/<string:filter>', methods=['GET'])
def get_spotify_conversion_rate(artist_id, date_end, filter):
    try:
        conversion_rate = SpotifyController.get_conversion_rate(artist_id, date_end, filter)
        return jsonify(conversion_rate), 200
    except Exception as e:
        return jsonify({'err': str(e)}), 500
