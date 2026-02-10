from models.artist_model import Artists
from models.tenant_model import Tenant
from flask import jsonify, request
import datetime
import json
from services.artist_service import ArtistService


class ArtistsController:

    def get_artist_by_id(artist_id):
        # Validate required parameters
        if not artist_id:
            return jsonify({"error": "Missing artist_id parameter"}), 400
        # <field name: field value>
        artist = Artists.objects(id=artist_id).exclude("id").first()
        # convert querySet to json use to_json()
        # use json.loads() to get dictionary
        if artist:
            return jsonify({
                "status": "success",
                "message": "Artist retrieved successfully",
                "data": json.loads(artist.to_json())
            }), 200
        else:
            return jsonify({
                "status": "error",
                "message": "Artist not found"
            }), 404

    def get_artists_by_tenant_id(tenant_id):
        # Validate required parameters
        if not tenant_id:
            return jsonify({"err": "Tenant ID is required"}), 400

        try:
            artists = Tenant.objects(id=tenant_id).first()
            if not artists:
                return jsonify({
                    "status": "success",
                    "message": "Artists retrieved successfully",
                    "data": artists.to_json()
                }), 200
        except Exception as e:
            return jsonify({
                "status": "error",
                "message": str(e)
            }), 500

    @staticmethod
    def get_all_artists():
        try:
            artists = Artists.objects().exclude("id")

            return jsonify({
                "status": "success",
                "message": "Artists retrieved successfully",
                "data": json.loads(artists.to_json())
            }), 200
        except Exception as e:
            return jsonify({
                "status": "error",
                "message": str(e)
            }), 500

    def get_artist_info(artist_id):
        # Validate required parameters
        if not artist_id:
            return jsonify({"err": "Missing artist_id parameter"}), 400

        try:
            new_artist_id = str(artist_id)

            pipeline = [
                {"$match": {
                    "artist_id": new_artist_id
                }},
                {"$project": {
                    "_id": 0,
                    "artist_id": "$artist_id",
                    "artist": "$english_name",
                    "korean_name": "$korean_name",
                    "debut_year": "$debut_year",
                    "nation": "$nation",
                    "pronouns": "$pronouns",
                    "type": "$type",
                    "birth": "$birth",
                    "fandom": "$fandom",
                    "belong_group": "$belong_group",
                    "instagram_id": "$instagram_id",
                    "instagram_user": "$instagram_user",
                    "threads": "$threads",
                    "youtube_id": "$youtube_id",
                    "tiktok_id": "$tiktok_id",
                    "spotify_id": "$spotify_id",
                    "melon_id": "$melon_id",
                    "genie_id": "$genie_id",
                    "qq_id": "$qq_id",
                    "bilibili_id": "$bilibili_id",
                    "weibo_id": "$weibo_id",
                    "image": "$image_url"
                }}
            ]

            results = Artists.objects().aggregate(pipeline)
            result = list(results)

            # Check if we got any results
            if not result:
                return jsonify({
                    "status": "success",
                    "data": [],
                    "message": "No data found for the specific artist id"
                }), 200

            return jsonify({
                "status": "success",
                "data": result
            }), 200
        except Exception as e:
            return jsonify({
                "status": "error",
                "err": str(e)
            }), 500

    @staticmethod
    def new_get_artist_info(artist_id):
        try:
            data = ArtistService.get_artist_info(artist_id)

            return jsonify({
                "status": "success",
                "data": data,
                "count": len(data)
            }), 200

        except ValueError as e:
            return jsonify({
                "status": "error",
                "error_code": "INVALID_PARAMETER",
                "message": str(e)
            }), 400
        except Exception as e:
            return jsonify({
                "status": "error",
                "error_code": "INTERNAL_SERVER_ERROR",
                "message": str(e)
            }), 500
