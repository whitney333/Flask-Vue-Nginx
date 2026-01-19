'''
updated: 2025-08-04
artist controller
- create artist (/v1/artist) -> POST
    - args:
        - tenant_id: string
        - english_name: string
        - korean_name: string
        - debut_year: int
        - nation: string
        - pronouns: string
        - type: list of strings
        - birth: datetime
        - fandom: string
        - instagram_id: string
        - threads: boolean
        - youtube_id: string
        - tiktok_id: string
        - spotify_id: string
        - melon_id: string
        - bilibili_id: string
        - image_url: string
    - return: artist object
    - error:
        - 400: bad request
        - 404: tenant not found
        - 500: internal server error
- get artist by id (/v1/artist/<string:artist_id>) -> GET
    - args:
        - artist_id: string
    - return: artist object
    - error:
        - 404: artist not found
        - 500: internal server error
- get artists by tenant id (/v1/artist/tenant/<string:tenant_id>) -> GET
    - args:
        - tenant_id: string
    - return: list of artist objects
    - error:
        - 404: tenant not found
        - 500: internal server error
- get all artists (/v1/artist/all) -> GET
    - args:
    - return: list of artist objects
    - error:
        - 500: internal server error
'''

from models.artist_model import Artist
from models.tenant_model import Tenant
from models.instagram_model import Instagram
from models.youtube_model import Youtube
from models.tiktok_model import Tiktok
from models.spotify_model import Spotify
from models.melon_model import Melon
from models.bilibili_model import Bilibili
from flask import request, jsonify

class ArtistController:

    def create_artist():
        try:
            data = request.get_json()
            tenant_id = data.get("tenant_id")
            english_name = data.get("english_name")
            korean_name = data.get("korean_name")
            debut_year = data.get("debut_year")
            nation = data.get("nation")
            pronouns = data.get("pronouns")
            type = data.get("type")
            birth = data.get("birth")
            fandom = data.get("fandom")
            instagram_id = data.get("instagram_id")
            threads = data.get("threads")
            youtube_id = data.get("youtube_id")
            tiktok_id = data.get("tiktok_id")
            spotify_id = data.get("spotify_id")
            melon_id = data.get("melon_id")
            bilibili_id = data.get("bilibili_id")
            image_url = data.get("image_url")

            if not tenant_id:
                return jsonify({"error": "Tenant ID is required"}), 400
            tenant = Tenant.objects(id=tenant_id).first()
            if not tenant:
                return jsonify({"error": "Tenant not found"}), 404

            if not instagram_id:
                instagram = None
            else:
                instagram = Instagram.objects(id=instagram_id).first()
                if not instagram:
                    return jsonify({"error": "Instagram not found"}), 404

            if not youtube_id:
                youtube = None
            else:
                youtube = Youtube.objects(id=youtube_id).first()
                if not youtube:
                    return jsonify({"error": "Youtube not found"}), 404

            if not tiktok_id:
                tiktok = None
            else:
                tiktok = Tiktok.objects(id=tiktok_id).first()
                if not tiktok:
                    return jsonify({"error": "Tiktok not found"}), 404

            if not spotify_id:
                spotify = None
            else:
                spotify = Spotify.objects(id=spotify_id).first()
                if not spotify:
                    return jsonify({"error": "Spotify not found"}), 404

            if not melon_id:
                melon = None
            else:
                melon = Melon.objects(id=melon_id).first()
                if not melon:
                    return jsonify({"error": "Melon not found"}), 404

            if not bilibili_id:
                bilibili = None
            else:
                bilibili = Bilibili.objects(id=bilibili_id).first()
                if not bilibili:
                    return jsonify({"error": "Bilibili not found"}), 404

            if not english_name:
                return jsonify({"error": "English name is required"}), 400
            if not korean_name:
                return jsonify({"error": "Korean name is required"}), 400
            if not nation:
                return jsonify({"error": "Nation is required"}), 400
            if not pronouns:
                return jsonify({"error": "Pronouns is required"}), 400
            if not type:
                return jsonify({"error": "Type is required"}), 400
            
            new_artist = Artist(
                tenant = tenant,
                english_name = english_name,
                korean_name = korean_name,
                debut_year = debut_year,
                nation = nation,
                pronouns = pronouns,
                type = type,
                birth = birth,
                fandom = fandom,
                instagram = instagram,
                threads = threads,
                youtube = youtube,
                tiktok = tiktok,
                spotify = spotify,
                melon = melon,
                bilibili = bilibili,
                image_url = image_url,
            )

            new_artist.save()
            return jsonify({
                "status": "success",
                "message": "Artist created successfully",
                "data": new_artist.to_json(),
            }), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    def get_artist_by_id(artist_id):
        try:
            artist = Artist.objects(id=artist_id).first()
            if artist:
                return jsonify({
                    "status": "success",
                    "message": "Artist retrieved successfully",
                    "data": artist.to_json(),
                }), 200
            else:
                return jsonify({"error": "Artist not found"}), 404
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    def get_artists_by_tenant_id(tenant_id):
        if not tenant_id:
            return jsonify({"error": "Tenant ID is required"}), 400
        try:
            tenant = Tenant.objects(id=tenant_id).first()
            if not tenant:
                return jsonify({"error": "Tenant not found"}), 404
            artists = Artist.objects(tenant=tenant)
            return jsonify({
                "status": "success",
                "message": "Artists retrieved successfully",
                "data": [artist.to_json() for artist in artists],
            }), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    def get_all_artists():
        try:
            artists = Artist.objects()
            return jsonify({
                "status": "success",
                "message": "Artists retrieved successfully",
                "data": [artist.to_json() for artist in artists],
            }), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
