from flask import Blueprint, jsonify, request
from flask_restful import Resource, reqparse, Api
from controllers.spotify_controller import SpotifyController

spotify_bp = Blueprint('spotify', __name__)
spotify_api = Api(spotify_bp)

# spotify follower route
@spotify_bp.route('/follower', methods=['GET'])
def get_spotify_follower():
    artist_id = request.args.get('artist_id', type=str)
    date_end = request.args.get('date_end', type=str)
    filter = request.args.get('filter', type=str)

    follower = SpotifyController.get_follower(artist_id, date_end, filter)

    return follower

# spotify monthly_listener route
@spotify_bp.route('/monthly_listener', methods=['GET'])
def get_spotify_monthly_listener():
    artist_id = request.args.get('artist_id', type=str)
    date_end = request.args.get('date_end', type=str)
    filter = request.args.get('filter', type=str)

    listener = SpotifyController.get_monthly_listener(artist_id, date_end, filter)

    return listener

# spotify popularity route
@spotify_bp.route('/popularity', methods=['GET'])
def get_spotify_popularity():
    artist_id = request.args.get('artist_id', type=str)
    date_end = request.args.get('date_end', type=str)
    filter = request.args.get('filter', type=str)

    popularity = SpotifyController.get_popularity(artist_id, date_end, filter)

    return popularity

# spotify fan conversion rate route
@spotify_bp.route('/conversion_rate', methods=['GET'])
def get_spotify_conversion_rate():
    artist_id = request.args.get('artist_id', type=str)
    date_end = request.args.get('date_end', type=str)
    filter = request.args.get('filter', type=str)

    conversion_rate = SpotifyController.get_conversion_rate(artist_id, date_end, filter)

    return conversion_rate
