from models.billboard_model import BillboardCharts


class BillboardService:
    @staticmethod
    def get_trending_artist_chart_score(year, week):
        if not year or not week:
            raise ValueError("year and week are required")

        year = str(year)
        week = int(week)
        pipeline = [
            {"$match": {
                "year": year
            }},
            {"$match": {
                "week": week
            }},
            {"$project": {
                "_id": 0,
                "datetime": "$datetime",
                "year": "$year",
                "month": "$month",
                "day": "$day",
                "week": "$week",
                "bb_chart": {
                    "$map": {
                        "input": "$data",
                        "as": "bb_item",
                        "in": {
                            "rank": {"$toInt": "$$bb_item.ranking"},
                            "artist": "$$bb_item.artist"
                        }
                    }
                }
            }},
            # calculate score
            {"$addFields": {
                "bb_chart": {
                    "$map": {
                        "input": "$bb_chart",
                        "as": "bb_chart",
                        "in": {
                            "$mergeObjects": [
                                "$$bb_chart",
                                {"bb_score": {
                                    "$subtract": [
                                        {"$toInt": 201},
                                        "$$bb_chart.rank"
                                    ]
                                }}
                            ]
                        }
                    }
                }
            }},
            {"$unwind": "$bb_chart"},
            {"$project": {
                "datetime": "$datetime",
                "year": "$year",
                "month": "$month",
                "day": "$day",
                "week": "$week",
                "rank": "$bb_chart.rank",
                "artist": "$bb_chart.artist",
                "billboard_score": "$bb_chart.bb_score"
            }},
            {"$group": {
                "_id": "$artist",
                "_all": {"$addToSet": "$$ROOT"},
                "year": {"$first": "$year"},
                "month": {"$first": "$month"},
                "day": {"$first": "$day"},
                "week": {"$first": "$week"},
                "bb_score_list": {"$addToSet": "$billboard_score"},
                "bb_artist": {"$first": "$artist"}
            }},
            # calculate billboard total score
            {"$project": {
                "_id": 0,
                "year": "$year",
                "month": "$month",
                "day": "$day",
                "week": "$week",
                "artist": "$bb_artist",
                "billboard_score": {
                    "$reduce": {
                        "input": "$bb_score_list",
                        "initialValue": 0,
                        "in": {
                            "$add": [{"$toInt": "$$value"}, "$$this"]
                        }
                    }
                }
            }},
            {"$sort": {"billboard_score": -1}}
        ]

        results = BillboardCharts.objects().aggregate(pipeline)
        result = []
        for item in results:
            result.append(item)

        return result
