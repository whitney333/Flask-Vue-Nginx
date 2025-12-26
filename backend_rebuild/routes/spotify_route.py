from flask import Blueprint, jsonify, request
from flask_restful import Resource, reqparse, Api
from controllers.spotify_controller import SpotifyController
from libs.utils import auth_required

spotify_bp = Blueprint('spotify', __name__)
spotify_api = Api(spotify_bp)

# spotify follower route
@spotify_bp.route('/v1/follower', methods=['GET'])
def get_spotify_follower():
    artist_id = request.args.get('artist_id', type=str)
    date_end = request.args.get('date_end', type=str)
    filter = request.args.get('filter', type=str)

    follower = SpotifyController.get_follower(artist_id, date_end, filter)

    return follower

# spotify monthly_listener route
@spotify_bp.route('/v1/monthly-listener', methods=['GET'])
def get_spotify_monthly_listener():
    artist_id = request.args.get('artist_id', type=str)
    date_end = request.args.get('date_end', type=str)
    filter = request.args.get('filter', type=str)

    listener = SpotifyController.get_monthly_listener(artist_id, date_end, filter)

    return listener

# spotify popularity route
@spotify_bp.route('/v1/popularity', methods=['GET'])
def get_spotify_popularity():
    artist_id = request.args.get('artist_id', type=str)
    date_end = request.args.get('date_end', type=str)
    filter = request.args.get('filter', type=str)

    popularity = SpotifyController.get_popularity(artist_id, date_end, filter)

    return popularity

# spotify fan conversion rate route
@spotify_bp.route('/v1/conversion-rate', methods=['GET'])
def get_spotify_conversion_rate():
    artist_id = request.args.get('artist_id', type=str)
    date_end = request.args.get('date_end', type=str)
    filter = request.args.get('filter', type=str)

    conversion_rate = SpotifyController.get_conversion_rate(artist_id, date_end, filter)

    return conversion_rate

@spotify_bp.route('/v1/top-city', methods=['GET'])
def get_spotify_top_five_city():
    artist_id = request.args.get('artist_id', type=str)

    top_five_city = SpotifyController.get_top_five_city(artist_id)

    return top_five_city

@spotify_bp.route('/v1/country/top-tracks', methods=['GET'])
def get_top_tracks_by_country():
    artist_id = request.args.get('artist_id', type=str)
    country = request.args.get('country', type=str)
    top_tracks_by_country = SpotifyController.get_top_tracks_by_country(artist_id, country)

    return top_tracks_by_country

@spotify_bp.route('/v1/region/top-tracks', methods=['GET'])
def get_top_tracks_by_region():
    artist_id = request.args.get('artist_id', type=str)
    top_tracks_by_region = SpotifyController.get_top_tracks_by_region(artist_id)

    return top_tracks_by_region

@spotify_bp.route("/v1/follower/growth", methods=["GET"])
def get_spotify_follower_growth():
    artist_id = request.args.get('artist_id', type=str)
    campaign_start = request.args.get('start', type=str)

    return SpotifyController.get_spotify_follower_growth(artist_id, campaign_start)

@spotify_bp.route("/v1/monthly-listener/growth", methods=["GET"])
def get_spotify_monthly_listener_growth():
    artist_id = request.args.get('artist_id', type=str)
    campaign_start = request.args.get('start', type=str)

    return SpotifyController.get_spotify_monthly_listener_by_artist_id(artist_id, campaign_start)

@spotify_bp.route("/v1/popularity/growth", methods=["GET"])
def get_spotify_popularity_growth():
    artist_id = request.args.get('artist_id', type=str)
    campaign_start = request.args.get('start', type=str)

    return SpotifyController.get_spotify_popularity_growth(artist_id, campaign_start)

@spotify_bp.route("/v1/top-city/growth", methods=["GET"])
def get_spotify_top_city_growth():
    artist_id = request.args.get('artist_id', type=str)
    campaign_start = request.args.get('start', type=str)

    return SpotifyController.get_spotify_top_five_city_growth(artist_id, campaign_start)

#################### v2 Endpoint ####################

@spotify_bp.route("/v2/follower/<string:artist_id>", methods=["GET"])
@auth_required
def get_spotify_follower_by_artist_id(artist_id):
    result = SpotifyController.get_spotify_follower_by_artist_id(artist_id)

    return result

@spotify_bp.route("/v2/monthly-listener/<string:artist_id>", methods=["GET"])
@auth_required
def get_spotify_monthly_listener_by_artist_id(artist_id):
    result = SpotifyController.get_spotify_monthly_listener_by_artist_id(artist_id)

    return result

@spotify_bp.route("/v2/popularity/<string:artist_id>", methods=['GET'])
@auth_required
def get_spotify_popularity_by_artist_id(artist_id):
    result = SpotifyController.get_spotify_popularity_by_artist_id(artist_id)

    return result

@spotify_bp.route("/v2/conversion-rate/<string:artist_id>", methods=['GET'])
@auth_required
def get_spotify_conversion_rate_by_artist_id(artist_id):
    result = SpotifyController.get_spotify_conversion_rate_by_artist_id(artist_id)

    return result

@spotify_bp.route("/v2/top-city/<string:artist_id>", methods=['GET'])
@auth_required
def get_spotify_top_city_by_artist_id(artist_id):
    result = SpotifyController.get_spotify_top_five_city_by_artist_id(artist_id)

    return result

@spotify_bp.route("/v2/country/top-tracks/<string:artist_id>", methods=['GET'])
@auth_required
def get_spotify_top_tracks_by_country_by_artist_id(artist_id):
    result = SpotifyController.get_spotify_top_tracks_by_country_by_artist_id(artist_id)

    return result
