from controllers.trending_artist_controller import TrendingArtistController
from flask import Blueprint, jsonify, request
from flask_restful import Resource, reqparse, Api

trending_artist_bp = Blueprint('trending_artist', __name__)
trending_artist_api = Api(trending_artist_bp)

### Music Score Section ###
@trending_artist_bp.route('/spotify-chart-score', methods=['GET'])
def spotify_chart_score():
    country = request.args.get('country', default=None)
    year = request.args.get('year', type=str)
    week = request.args.get('week', type=int)

    return TrendingArtistController.get_spotify_charts_score(country, year, week)

@trending_artist_bp.route('/spotify-popularity', methods=['GET'])
def spotify_popularity():
    spotify_pop_score = TrendingArtistController.get_spotify_popularity_score()

    return spotify_pop_score

@trending_artist_bp.route('/spotify-score', methods=['GET'])
def total_spotify_score():
    country = request.args.get('country', default=None)
    year = request.args.get('year', type=str)
    week = request.args.get('week', type=int)

    merge_spotify_score = TrendingArtistController.merge_spotify_score(country, year, week)

    return merge_spotify_score

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

@trending_artist_bp.route('/merge-music-score', methods=['GET'])
def merge_music_score():
    country = request.args.get('country', default=None)
    year = request.args.get('year', type=str)
    week = request.args.get('week', type=int)

    merge_music_score = TrendingArtistController.merge_music_scores(country, year, week)

    return merge_music_score

@trending_artist_bp.route('/music-score', methods=['GET'])
def total_music_score():
    country = request.args.get('country', default=None)
    year = request.args.get('year', type=str)
    week = request.args.get('week', type=int)

    music_score = TrendingArtistController.get_music_score(country, year, week)

    return music_score

### SNS Score Section ###
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

@trending_artist_bp.route('/instagram-follower-growth', methods=['GET'])
def instagram_follower_growth():
    artist_id = request.args.get('artist_id', type=str)
    
    ig_follower_growth_score = TrendingArtistController.get_instagram_7day_follower_growth(artist_id)
    
    return ig_follower_growth_score

@trending_artist_bp.route('/instagram-engagement', methods=['GET'])
def instagram_engagement():
    artist_id = request.args.get('artist_id', type=str)

    ig_engage_score = TrendingArtistController.get_instagram_engage(artist_id)

    return ig_engage_score

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
    sns_scores = TrendingArtistController.get_sns_score()

    return sns_scores

### Drama Score Section ###
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
    dramas = TrendingArtistController.get_dramas(year)

    return dramas

@trending_artist_bp.route('/artist', methods=['GET'])
def _get_artist_id():
    artist_id = request.args.get('id', type=str)

    artist = TrendingArtistController.get_db_artist_ids(artist_id)

    return artist

@trending_artist_bp.route('/f-ost-score', methods=['GET'])
def group_ost_score_by_drama():
    year = request.args.get('year', type=str)
    week = request.args.get('week', type=int)

    result = TrendingArtistController.filter_ost_by_drama_name(year, week)

    return result

@trending_artist_bp.route('/merge-drama-score', methods=['GET'])
def _drama_score():
    country = request.args.get('country', default=None)
    year = request.args.get('year', type=str)
    week = request.args.get('week', type=int)

    _drama_score = TrendingArtistController.merge_drama_score(country, year, week)

    return _drama_score

@trending_artist_bp.route('/drama-score', methods=['GET'])
def total_drama():
    country = request.args.get('country', default=None)
    year = request.args.get('year', type=str)
    week = request.args.get('week', type=int)

    drama_scores = TrendingArtistController.get_drama_score(country, year, week)

    return drama_scores

@trending_artist_bp.route('/pre-drama-score', methods=['GET'])
def pre_drama_score():
    country = request.args.get('country', default=None)
    year = request.args.get('year', type=str)
    week = request.args.get('week', type=int)

    pre_drama_scores = TrendingArtistController.get_pre_drama_score(country, year, week)

    return pre_drama_scores

@trending_artist_bp.route('/artists', methods=['GET'])
def artists():
    artists = TrendingArtistController.query_db_artist()

    return artists

@trending_artist_bp.route('/popularity', methods=['GET'])
def overall_popularity():
    country = request.args.get('country', default=None)
    year = request.args.get('year', type=str)
    week = request.args.get('week', type=int)
    type = request.args.get('type', type=str)

    popularity = TrendingArtistController.calculate_overall_popularity(country, year, week, type)

    return popularity
