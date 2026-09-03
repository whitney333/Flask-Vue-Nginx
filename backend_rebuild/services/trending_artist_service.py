from models.trending_artist_score_model import ArtistPopularity


class TrendingArtistService:
    SCORE_FIELD_MAP = {
        "overall": "-popularity_score",
        "music": "-music_score",
        "sns": "-sns_score",
        "drama": "-drama_score",
    }

    @staticmethod
    def get_trending_artists(country, year, week, artist_type="all", limit=100):
        country = country.upper()

        queryset = ArtistPopularity.objects(
            country=country,
            year=int(year),
            week=int(week)
        )

        artist_type = (artist_type or "all").strip().title()

        if artist_type != "All":
            queryset = queryset.filter(type=artist_type)

        return queryset.order_by("-popularity_score")[:limit]

    @staticmethod
    def get_country_rank_map(artist_id, year, week):
        rows = ArtistPopularity.objects(
            artist_id=artist_id,
            year=int(year),
            week=int(week)
        ).only("country", "rank", "previous_rank", "rank_change", "change_type")

        rank_map = {}
        change_map = {}

        for row in rows:
            country = row.country.lower()
            rank_map[country] = row.rank
            change_map[country] = {
                "previous_rank": row.previous_rank,
                "rank_change": row.rank_change,
                "change_type": row.change_type,
            }

        return {
            "artist_id": str(artist_id),
            "year": year,
            "week": week,
            "rank": rank_map,
            "change": change_map
        }
