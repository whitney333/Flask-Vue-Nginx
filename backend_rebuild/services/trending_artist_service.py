from models.trending_artist_music_model import TrendingArtistMusicScore
from models.trending_artist_sns_model import TrendingArtistSnsScore
from models.trending_artist_score_model import ArtistPopularity


class TrendingArtistService:
    SCORE_FIELD_MAP = {
        "overall": "-popularity_score",
        "music": "-music_score",
        "sns": "-sns_score",
        "drama": "-drama_score",
    }

    @staticmethod
    def get_trending_artists(country, year, week, limit=100):
        country = country.upper()

        queryset = ArtistPopularity.objects(
            country=country,
            year=int(year),
            week=int(week)
        ).order_by("-popularity_score")

        return queryset[:limit]

    @staticmethod
    def get_country_rank_map(artist_id, year, week):
        rows = ArtistPopularity.objects(
            artist_id=artist_id,
            year=int(year),
            week=int(week)
        ).only("country", "rank")

        rank_map = {}

        for row in rows:
            rank_map[row.country.lower()] = row.rank

        return {
            "artist_id": str(artist_id),
            "year": year,
            "week": week,
            "rank": rank_map
        }
