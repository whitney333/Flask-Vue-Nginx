from flask import request, jsonify
from models.artist_model import Artists
from models.trending_artist_score_model import ArtistPopularity
from services.trending_artist_service import TrendingArtistService

from services.trending_artist_service import TrendingArtistService

class TrendingArtistController:
    @staticmethod
    def get_trending_artist_popularity_score(country, year, week):

        if not all([year, week]):
            return jsonify({
                "err": "Missing required parameters"
            }), 400

        country = country.upper() if country else "GLOBAL"

        try:

            # =========================
            # call service (IMPORTANT FIX)
            # =========================
            results = TrendingArtistService.get_trending_artists(
                country=country,
                year=year,
                week=week
            )

            artists = []

            for doc in results:
                artists.append({
                    "rank": doc.rank,
                    "artist_id": str(doc.artist_id.id) if doc.artist_id else None,
                    "english_name": doc.english_name,
                    "korean_name": doc.korean_name,
                    "image": doc.image,
                    "type": doc.type,

                    # =========================
                    # unified scores (NOT sns-only anymore)
                    # =========================
                    "popularity_score": doc.popularity_score,
                    "music_score": doc.music_score,
                    "sns_score": doc.sns_score,
                    "drama_score": doc.drama_score,
                })

            return jsonify({
                "country": country,
                "year": year,
                "week": week,
                "total": len(artists),
                "artists": artists
            }), 200

        except Exception as e:
            return jsonify({
                "err": str(e)
            }), 500

    @staticmethod
    def get_trending_artist_rank_map(artist_id, year, week):
        if not all([artist_id, year, week]):
            return jsonify({
                "err": "Missing required parameters"
            }), 400

        try:
            results = TrendingArtistService.get_country_rank_map(
                artist_id=artist_id,
                year=year,
                week=week
            )
            return jsonify({
                "data": results
            }), 200
        except Exception as e:
            return jsonify({
                "err": str(e)
            }), 500
