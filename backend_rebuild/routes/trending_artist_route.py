from controllers.trending_artist_controller import TrendingArtistController
from flask import Blueprint, jsonify, request
from flask_restful import Resource, reqparse, Api

trending_artist_bp = Blueprint('trending_artist', __name__)
trending_artist_api = Api(trending_artist_bp)

@trending_artist_bp.route('/spotify-score', methods=['GET'])
def spotify_chart_score():
    country = request.args.get('country', default=None)
    year = request.args.get('year', type=str)
    week = request.args.get('week', type=int)

    return TrendingArtistController.get_spotify_charts_score(country, year, week)

@trending_artist_bp.route('/youtube-score', methods=['GET'])
def youtube_chart_score():
    country = request.args.get('country', default=None)
    year = request.args.get('year', type=str)
    week = request.args.get('week', type=int)

    return TrendingArtistController.get_youtube_charts_score(country, year, week)

@trending_artist_bp.route('/billboard-score', methods=['GET'])
def billboard_chart_score():
    year = request.args.get('year', type=str)
    week = request.args.get('week', type=int)

    return TrendingArtistController.get_billboard_charts_score(year, week)

@trending_artist_bp.route('/music-score', methods=['GET'])
def total_music_score():
    country = request.args.get('country', default=None)
    year = request.args.get('year', type=str)
    week = request.args.get('week', type=int)

    music_score = TrendingArtistController.get_music_score(country, year, week)

    return music_score

@trending_artist_bp.route('/tiktok-sns-score', methods=['GET'])
def tiktok_sns_score():
    artist_id = request.args.get('artist_id', type=str)

    tk_sns_score = TrendingArtistController.get_tiktok_score(artist_id)

    return tk_sns_score

@trending_artist_bp.route('/youtube-sns-score', methods=['GET'])
def youtube_sns_score():
    artist_id = request.args.get('artist_id', type=str)

    yt_sns_score = TrendingArtistController.get_youtube_score(artist_id)

    return yt_sns_score

@trending_artist_bp.route('/instagram-sns-score', methods=['GET'])
def instagram_sns_score():
    artist_id = request.args.get('artist_id', type=str)

    ig_sns_score = TrendingArtistController.get_instagram_score(artist_id)

    return ig_sns_score

@trending_artist_bp.route('/merge-sns-score', methods=['GET'])
def get_sns_score():
    """
    Based on music chart data
    :return:
    """
    country = request.args.get('country', default=None)
    year = request.args.get('year', type=str)
    week = request.args.get('week', type=int)

    all_sns_score = TrendingArtistController.merge_all_sns_scores(country, year, week)

    return all_sns_score

@trending_artist_bp.route('/pre-sns-score', methods=['GET'])
def _sns_score():
    sns_score = TrendingArtistController.get_sns_score()

    return sns_score

@trending_artist_bp.route('/sns-score', methods=['GET'])
def total_sns_score():
    sns_scores = TrendingArtistController.get_total_sns_score()

    return sns_scores

@trending_artist_bp.route('/netflix-score', methods=['GET'])
def netflix_chart_score():
    country = request.args.get('country', default=None)
    year = request.args.get('year', type=str)
    week = request.args.get('week', type=int)

    netflix_chart = TrendingArtistController.get_netflix_chart(country, year, week)

    return netflix_chart

@trending_artist_bp.route('/ost-score', methods=['GET'])
def spotify_ost_score():
    year = request.args.get('year', type=str)
    week = request.args.get('week', type=int)

    ost_score = TrendingArtistController.get_spotify_ost(year, week)

    return ost_score

@trending_artist_bp.route('/dramas', methods=['GET'])
def all_drama():
    year = request.args.get('year', type=int)
    dramas = TrendingArtistController.get_all_drama(year)

    return dramas

@trending_artist_bp.route('/merge-drama-score', methods=['GET'])
def _drama_score():
    country = request.args.get('country', default=None)
    year = request.args.get('year', type=str)
    week = request.args.get('week', type=int)

    drama_score = TrendingArtistController.get_drama_score(country, year, week)

    return drama_score

########################################################
# V1 endpoints for Trending Artists feature
########################################################

@trending_artist_bp.route('/v1/rank/<string:country>', methods=['GET'])
def get_trending_rank(country):
    """
    Get ranked list of artists by popularity for a given country/region.
    Query params: year, week
    Returns: List of artists sorted by popularity with rank
    """
    year = request.args.get('year', type=int)
    week = request.args.get('week', type=int)

    return TrendingArtistController.get_trending_rank(country, year, week)

@trending_artist_bp.route('/v1/artist/<string:artist_id>/scores', methods=['GET'])
def get_artist_scores(artist_id):
    """
    Get popularity, SNS, music, and drama scores for an artist.
    For artist details, use /api/artist/v1/artist/<artist_id> instead.
    Query params: year (required), week (required)
    Returns: Artist scores (popularity, total_music_score, total_sns_score, total_drama_score, global_rank)
    """
    year = request.args.get('year', type=int)
    week = request.args.get('week', type=int)

    return TrendingArtistController.get_artist_scores(artist_id, year, week)
