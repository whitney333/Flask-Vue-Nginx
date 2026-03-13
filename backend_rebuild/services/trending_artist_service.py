from models.trending_artist_music_model import TrendingArtistMusicScore
from models.trending_artist_sns_model import TrendingArtistSnsScore


class TrendingArtistService:
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
