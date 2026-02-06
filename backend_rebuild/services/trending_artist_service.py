from .instagram_service import InstagramService
from .youtube_service import YoutubeService
from .tiktok_service import TiktokService
from .spotify_service import SpotifyService
from .artist_service import ArtistService
from .billboard_service import BillboardService
from .netflix_service import NetflixService
import re
from collections import defaultdict


REMOVE_KEYWORDS = [
    "ost",
    "original soundtrack",
    "soundtrack",
    "part",
    "season",
    "시즌",
    "pt",
    "vol",
    "limited series"
]

def normalize_artist_name(name: str):
    if not name:
        return ""

    name = name.lower()
    name = name.strip()

    # remove feat / featuring / with / x
    name = re.split(r"\s(feat\.?|featuring|with|x|&)\s", name)[0]

    # remove non-string
    name = re.sub(r"[^a-z0-9가-힣]", "", name)

    return name

def normalize_drama_name(name: str):
    if not name:
        return ""

    name = name.lower()

    # remove bracket content
    name = re.sub(r"\(.*?\)", "", name)

    # remove keywords
    for kw in REMOVE_KEYWORDS:
        name = re.sub(rf"\b{kw}\b.*", "", name)

    # remove symbols
    name = re.sub(r"[^a-z0-9가-힣\s]", " ", name)

    # normalize spaces
    name = re.sub(r"\s+", " ", name).strip()

    return name

class TrendingArtistService:
    """
    Calculate the Trending Artist Score based on Music Score, SNS Score, and Drama Score.
    The Music Score includes Spotify popularity, Spotify weekly charts,
    YouTube weekly Top Songs charts,
    and the Billboard Global 200 chart
    """

    @classmethod
    def get_music_score(cls, country=None, year=None, week=None, top=100):
        artists = ArtistService.get_db_artist()
        if not artists:
            return []

        spotify_ids = [a.get("spotify_id") for a in artists if a.get("spotify_id")]

        # Spotify popularity
        popularity_map = SpotifyService.get_trending_artist_popularity(spotify_ids)

        # init dict to prevent later KeyError
        spotify_chart_score_map = {}
        youtube_chart_score_map = {}
        billboard_map = {}

        if country and year and week:
            # Spotify chart
            sp_chart_results = SpotifyService.get_trending_artist_chart_score(country, year, week)
            spotify_chart_score_map = {str(c.get("spotify_id")): c.get("sp_chart_score", 0) for c in sp_chart_results}

            # YouTube chart
            yt_chart_results = YoutubeService.get_trending_artist_chart_score(country, year, week)
            youtube_chart_score_map = {str(c.get("channel_id")): c.get("yt_chart_score", 0) for c in yt_chart_results}

            # Billboard chart
            billboard_results = BillboardService.get_trending_artist_chart_score(year=year, week=week)
            # if billboard_results is None or blank list
            if billboard_results:
                billboard_map = {normalize_artist_name(c.get("artist", "")): c.get("billboard_score", 0)
                                 for c in billboard_results}

        #  merge
        results = []
        for artist in artists:
            artist_id = artist.get("artist_id")
            artist_name = artist.get("english_name") or artist.get("korean_name") or ""

            # spotify
            spotify_id = artist.get("spotify_id")
            sp_pop_score = popularity_map.get(spotify_id, 0)
            sp_chart_score = spotify_chart_score_map.get(spotify_id, 0)
            spotify_score = sp_pop_score + sp_chart_score

            # youtube
            youtube_id = artist.get("youtube_id")
            youtube_score = youtube_chart_score_map.get(youtube_id, 0)

            # billboard
            normalized_name = normalize_artist_name(artist_name)
            billboard_score = billboard_map.get(normalized_name, 0)

            # total music score
            music_score = spotify_score + youtube_score + billboard_score

            results.append({
                "_id": str(artist.get("_id")),
                "artist_id": artist_id,
                "artist_name": artist_name,

                "spotify": {
                    "popularity_score": sp_pop_score,
                    "chart_score": sp_chart_score,
                    "spotify_score": spotify_score
                },
                "youtube": {
                    "chart_score": youtube_score
                },
                "billboard": {
                    "chart_score": billboard_score
                },
                "music_score": music_score
            })

        # sort by music_score
        results.sort(key=lambda x: x["music_score"], reverse=True)

        return results[:top]

    @staticmethod
    def get_sns_score():
        pass

    @staticmethod
    def get_staging_drama_score(country, year, week):
        """
        Calculate drama score = ost score + netflix score
        (staging version)
        """
        # get netflix score
        netflix_rows = NetflixService.get_trending_artist_chart_score(
            country=country,
            year=year,
            week=week
        )

        # get ost score
        ost_rows = SpotifyService.get_trending_artist_ost_score(
            year=year,
            week=week
        )

        netflix_map = {
            normalize_drama_name(n["name"]): n
            for n in netflix_rows
        }

        ost_map = {
            normalize_drama_name(o["album"]): o
            for o in ost_rows
        }

        all_keys = set(netflix_map.keys()) | set(ost_map.keys())

        results = []
        for key in all_keys:
            netflix = netflix_map.get(key)
            ost = ost_map.get(key)

            result = {
                "normalized_name": key,
                "year": year,
                "week": week,
                "country": country,
                # Netflix
                "netflix_score": netflix["netflix_score"] if netflix else 0,
                "netflix_rank": netflix["rank"] if netflix else None,

                # OST
                "ost_score": ost["play_counts"] if ost else 0,

                # Final drama score
                "drama_score": (
                        (netflix["netflix_score"] if netflix else 0)
                        + (ost["play_counts"] if ost else 0)
                )
            }
            results.append(result)

        return results

    @staticmethod
    def get_drama_score(country, year, week):
        staging_rows = TrendingArtistService.get_staging_drama_score(
            country=country,
            year=year,
            week=week
        )

        grouped = defaultdict(lambda: {
            "netflix_score": 0,
            "ost_score": 0
        })

        for row in staging_rows:
            key = row["normalized_name"]

            grouped[key]["netflix_score"] = max(
                grouped[key]["netflix_score"],
                row.get("netflix_score", 0)
            )
            grouped[key]["ost_score"] += row.get("ost_score", 0)

        results = []
        for name, score in grouped.items():
            results.append({
                "name": name,
                "year": year,
                "week": week,
                "country": country,
                "netflix_score": score["netflix_score"],
                "ost_score": score["ost_score"],
                "drama_score": score["netflix_score"] + score["ost_score"]
            })

        return results
