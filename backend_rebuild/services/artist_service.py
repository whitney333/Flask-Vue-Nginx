from models.artist_model import Artists
from bson import ObjectId
from flask import jsonify


class ArtistService:

    @staticmethod
    def get_artist(artist_id):
        """
        get artist document
        """
        artist = Artists.objects(id=artist_id).first()
        if not artist:
            raise ValueError("Artist not found")
        return artist

    @staticmethod
    def get_artist_info(artist_id):
        artist = Artists.objects(
            id=ObjectId(artist_id)
        ).first()

        if not artist:
            return []

        return [{
            "_id": str(artist.id),
            "artist_id": artist.artist_id,
            "artist": artist.english_name,
            "korean_name": artist.korean_name,
            "debut_year": artist.debut_year,
            "nation": artist.nation,
            "pronouns": artist.pronouns,
            "type": artist.type,
            "birth": artist.birth,
            "fandom": artist.fandom,
            "belong_group": artist.belong_group,
            "instagram_id": artist.instagram_id,
            "instagram_user": artist.instagram_user,
            "threads": artist.threads,
            "youtube_id": artist.youtube_id,
            "tiktok_id": artist.tiktok_id,
            "spotify_id": artist.spotify_id,
            "melon_id": artist.melon_id,
            "genie_id": artist.genie_id,
            "apple_id": artist.apple_id,
            "bilibili_id": artist.bilibili_id,
            "weibo_id": artist.weibo_id,
            "image": artist.image_url
        }]

    @staticmethod
    def get_bilibili_id(artist_id):
        """
        return bilibili_id（for BilibiliService）
        """
        artist = ArtistService.get_artist(artist_id)

        if not artist.bilibili_id:
            raise ValueError("Missing bilibili_id")

        return artist.bilibili_id

    @staticmethod
    def get_instagram_id(artist_id):
        """
        return instagram_id（for InstagramService）
        """
        artist = ArtistService.get_artist(artist_id)

        if not artist.instagram_id:
            raise ValueError("Missing instagram_id")

        return artist.instagram_id

    @staticmethod
    def get_spotify_id(artist_id):
        """
        return spotify_id（for SpotifyService）
        """
        artist = ArtistService.get_artist(artist_id)

        if not artist.spotify_id:
            raise ValueError("Missing spotify_id")

        return artist.spotify_id

    @staticmethod
    def get_tiktok_id(artist_id):
        """
        return tiktok_id（for TiktokService）
        """
        artist = ArtistService.get_artist(artist_id)

        if not artist.tiktok_id:
            raise ValueError("Missing tiktok_id")

        return artist.tiktok_id

    @staticmethod
    def get_youtube_id(artist_id):
        """
        return youtube_id（for YoutubeService）
        """
        artist = ArtistService.get_artist(artist_id)

        if not artist.youtube_id:
            raise ValueError("Missing youtube_id")

        return artist.youtube_id

    @staticmethod
    def get_melon_id(artist_id):
        """
        return melon_id（for MelonService）
        """
        artist = ArtistService.get_artist(artist_id)

        if not artist.melon_id:
            raise ValueError("Missing melon_id")

        return artist.melon_id
