from models.netflix_model import NetflixCharts


class NetflixService:
    @staticmethod
    def get_trending_artist_chart_score(country, year, week):
        """
        Return netflix chart data for given country, year, week
        """
        if not country or not year or not week:
            raise ValueError("country, year and week are required")

        year = int(year)
        week = int(week)

        pipeline = [
            {
                "$match": {
                    "country": country
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "datetime": "$datetime",
                    "week": "$week",
                    "country": "$country",
                    "rank": "$rank",
                    "name": "$name",
                    "weeks_on_chart": "$weeks_on_chart"
                }
            },
            {
                "$addFields": {
                    "year": {
                        "$year": "$datetime"
                    }
                }
            },
            # match year & week
            {
                "$match": {
                    "year": int(year),
                    "week": int(week)
                }
            },
            # calculate rank score
            {
                "$addFields": {
                    "rank_score": {
                        "$subtract": [201, {"$toInt": "$rank"}]
                    }
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "year": "$year",
                    "week": "$week",
                    "country": "$country",
                    "rank": "$rank",
                    "netflix_score": {"$toInt": "$rank_score"},
                    "name": "$name",
                    "weeks_on_chart": "$weeks_on_chart"
                }
            }
        ]

        results = NetflixCharts.objects.aggregate(pipeline)
        return list(results)
