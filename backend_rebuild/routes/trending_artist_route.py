from controllers.trending_artist_controller import TrendingArtistController
from flask import Blueprint, jsonify, request
from flask_restful import Resource, reqparse, Api

trending_artist_bp = Blueprint('trending_artist', __name__)
trending_artist_api = Api(trending_artist_bp)

#################### v2 Endpoint ####################
@trending_artist_bp.route("/v2/popularity", methods=['GET'])
def get_artist_overall_popularity():
    country = request.args.get('country', default='GLOBAL')
    year = request.args.get('year', type=int)
    week = request.args.get('week', type=int)

    return TrendingArtistController.get_trending_artist_popularity_score(
        country,
        year,
        week
    )

@trending_artist_bp.route("/v2/ranks", methods=['GET'])
def get_artist_rank_map():
    artist_id = request.args.get('artist_id', type=str)
    year = request.args.get('year', type=str)
    week = request.args.get('week', type=int)

    results = TrendingArtistController.get_trending_artist_rank_map(artist_id, year, week)

    return results