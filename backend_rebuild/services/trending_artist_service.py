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

        # no_dereference: callers only need the artist ObjectId (doc.artist_id.id),
        # which is already stored on the score document. Without this, mongoengine
        # fetches the full Artists document for every row (N+1 round trips).
        queryset = ArtistPopularity.objects(
            country=country,
            year=int(year),
            week=int(week)
        ).no_dereference()

        artist_type = (artist_type or "all").strip().title()

        if artist_type != "All":
            queryset = queryset.filter(type=artist_type)

        return queryset.order_by("-popularity_score")[:limit]

    @staticmethod
    def get_trending_meta(country, year, week, artist_type="all"):
        """Row count and last update time for a week/country, for the list footer.

        Two cheap queries on the (country, year, week, popularity_score) index:
        a count and a top-1 sort on updated_at over at most a few hundred docs.
        """
        country = country.upper()

        queryset = ArtistPopularity.objects(
            country=country,
            year=int(year),
            week=int(week)
        )

        artist_type = (artist_type or "all").strip().title()

        if artist_type != "All":
            queryset = queryset.filter(type=artist_type)

        latest = queryset.only("updated_at").order_by("-updated_at").first()

        return {
            "total_available": queryset.count(),
            "updated_at": latest.updated_at.isoformat() if latest and latest.updated_at else None,
        }

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
