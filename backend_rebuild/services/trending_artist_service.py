from models.trending_artist_music_model import TrendingArtistMusicScore
from models.trending_artist_sns_model import TrendingArtistSnsScore
from models.trending_artist_score_model import TrendingArtistScore


class TrendingArtistService:
    SCORE_FIELD_MAP = {
        "overall": "-popularity_score",
        "music": "-music_score",
        "sns": "-sns_score",
        "drama": "-drama_score",
    }

    @staticmethod
    def get_music_score(country, year, week):
        country = country.upper() if country else None

        return TrendingArtistMusicScore.objects(
            country=country,
            year=str(year),
            week=int(week)
        ).order_by('-music_score')

    @staticmethod
    def get_sns_score(year, week):
        return TrendingArtistSnsScore.objects(
            year=int(year),
            week=int(week)
        ).order_by('-sns_score')

    @staticmethod
    def get_trending_artists(
            category="overall",
            country="GLOBAL",
            year=None,
            week=None,
            artist_type=None,
            limit=100
    ):
        country = country.upper()

        # =========================
        # sort field
        # =========================

        order_field = TrendingArtistService.SCORE_FIELD_MAP.get(
            category,
            "-popularity_score"
        )

        # =========================
        # base query
        # =========================

        queryset = TrendingArtistScore.objects(
            country=country,
            year=int(year),
            week=int(week)
        )

        # =========================
        # artist type filter
        # =========================

        if artist_type:
            queryset = queryset.filter(
                type=artist_type
            )

        # =========================
        # sorting
        # =========================

        queryset = queryset.order_by(
            order_field
        )[:limit]

        return queryset
