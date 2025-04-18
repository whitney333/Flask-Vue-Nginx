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

