from flask import request, jsonify
# music related data
from models.spotify_model import SpotifyCharts
from models.sns.youtube_model import YoutubeCharts
from models.billboard_model import BillboardCharts

# drama related data
from models.netflix_model import NetflixCharts

class TrendingArtistController:
    """
    Calculate Trending Artist Score from 3 aspects:
    1) Music Performance
        Includes: Spotify_Charts, Youtube_Charts, Billboard_Charts
    2) SNS Performance
        Includes:
    3) Drama Performance
        Includes: Netflix_Charts, Spotify_Ost
    """
    @staticmethod
    def get_spotify_charts_score(country, year, week):

        if not all([country, year, week]):
            return jsonify({'err': 'Missing required parameters'}), 400

        try:
            year = str(year)
            week = int(week)
            pipeline = [
            # match country
            {"$match": {
                "country": country
            }},
            # match year
            {"$match": {
                "year": year
            }},
            # match week
            {"$match": {
                "week": week
            }},
            {"$project": {
                "_id": 0,
                "datetime": "$datetime",
                "country": "$country",
                "year": "$year",
                "month": "$month",
                "day": "$day",
                "week": "$week",
                "spotify_weekly_top_songs": "$weekly_top_songs",
            }},
            {"$unwind": "$spotify_weekly_top_songs"},
            # calculate spotify score
            {"$project": {
                "datetime": "$datetime",
                "year": "$year",
                "month": "$month",
                "day": "$day",
                "week": "$week",
                "country": "$country",
                "sp_rank": {"$toInt": "$spotify_weekly_top_songs.rank"},
                # check song title
                "sp_song": "$spotify_weekly_top_songs.title",
                "sp_artist_id": "$spotify_weekly_top_songs.artist_id",
                "artist": {
                    "$trim": {
                        "input": "$spotify_weekly_top_songs.artist",
                        "chars": ","
                    }
                }
            }},
            {"$addFields": {
                "sp_score": {
                    "$subtract": [
                        {"$toInt": 201},
                        {"$toInt": "$sp_rank"}
                    ]
                }
            }},
            # group by artist, get total score
            {"$group": {
                "_id": "$sp_artist_id",
                "datetime": {"$first": "$datetime"},
                "year": {"$first": "$year"},
                "month": {"$first": "$month"},
                "day": {"$first": "$day"},
                "week": {"$first": "$week"},
                "country": {"$first": "$country"},
                "artist": {"$first": "$artist"},
                "sp_score_list": {"$addToSet": "$sp_score"}
            }},
            {"$project": {
                "sp_id": "$_id",
                "datetime": "$datetime",
                "year": "$year",
                "month": "$month",
                "day": "$day",
                "week": "$week",
                "country": "$country",
                "artist": "$artist",
                "sp_total_score": {
                    "$reduce": {
                        "input": "$sp_score_list",
                        "initialValue": 0,
                        "in": {"$add": [{"$toInt": "$$value"}, "$$this"]}
                    }
                }
            }},
            {"$sort": {"sp_total_score": -1}},
             # lookup artist
            {"$lookup": {
                "from": "artist",
                "localField": "sp_id",
                "foreignField": "spotify_id",
                "as": "artist_info"
            }},
            {"$unwind": "$artist_info"},
            # keep artist id from all platforms
            {"$project": {
                "_id": 0,
                "datetime": "$datetime",
                "year": "$year",
                "month": "$month",
                "day": "$day",
                "week": "$week",
                "country": "$country",
                "artist": "$artist",
                "sp_total_score": "$sp_total_score",
                "spotify_id": "$sp_id",
                "instagram_id": "$artist_info.instagram_id",
                "instagram_user": "$artist_info.instagram_user",
                "youtube_id": "$artist_info.youtube_id",
                "tiktok_id": "$artist_info.tiktok_id"
            }}
        ]

            results = SpotifyCharts.objects().aggregate(pipeline)

            result = []
            for item in results:
                result.append(item)

            return jsonify({
                'status': 'success',
                'data': result
            }), 200
        except Exception as e:
            return jsonify({'err': str(e)}), 500

    @staticmethod
    def get_youtube_charts_score(country, year, week):
        if not all([country, year, week]):
            return jsonify({'err': 'Missing required parameters'}), 400

        try:
            year = str(year)
            week = int(week)

            pipeline = [
                {"$match": {
                    "country": country
                }},
                {"$match": {
                    "year": year
                }},
                {"$match": {
                    "week": week
                }},
                {"$project": {
                    "country": "$country",
                    "datetime": "$datetime",
                    "year": "$year",
                    "month": "$month",
                    "day": "$day",
                    "week": "$week",
                    "yt_charts": {
                        "$map": {
                            "input": "$weekly_top_songs",
                            "as": "yt_item",
                            "in": {
                                "rank": {"$toInt": "$$yt_item.rank"},
                                "artist": "$$yt_item.artist",
                                "title": "$$yt_item.title"
                            }
                        }
                    }
                }},
                # calculate youtube charts score by artists first
                {"$addFields": {
                    "yt_charts": {
                        "$map": {
                            "input": "$yt_charts",
                            "as": "yt_chart",
                            "in": {
                                "$mergeObjects": [
                                    "$$yt_chart",
                                    {"yt_score": {
                                        "$subtract": [
                                            {"$toInt": 101},
                                            {"$toInt": "$$yt_chart.rank"}]
                                    }}
                                ]
                            }
                        }
                    }
                }},
                {"$unwind": "$yt_charts"},
                {"$project": {
                    "country": "$country",
                    "datetime": "$datetime",
                    "year": "$year",
                    "month": "$month",
                    "day": "$day",
                    "week": "$week",
                    "rank": "$yt_charts.rank",
                    "yt_score": "$yt_charts.yt_score",
                    "title": "$yt_charts.title",
                    "artist": "$yt_charts.artist",
                }},
                {"$group": {
                    "_id": "$artist",
                    "_all": {"$addToSet": "$$ROOT"},
                    "year": {"$first": "$year"},
                    "month": {"$first": "$month"},
                    "day": {"$first": "$day"},
                    "week": {"$first": "$week"},
                    "yt_score_list": {"$addToSet": "$yt_score"},
                    "yt_artist": {"$first": "$artist"}
                }},
                # calculate billboard total score
                {"$project": {
                    "_id": 0,
                    "year": "$year",
                    "month": "$month",
                    "day": "$day",
                    "week": "$week",
                    "artist": "$yt_artist",
                    "youtube_score": {
                        "$reduce": {
                            "input": "$yt_score_list",
                            "initialValue": 0,
                            "in": {
                                "$add": [{"$toInt": "$$value"}, "$$this"]
                            }
                        }
                    }
                }},
                {"$sort": {"youtube_score": -1}}
            ]

            results = YoutubeCharts.objects().aggregate(pipeline)
            result = []
            for item in results:
                result.append(item)

            return jsonify({
                'status': 'success',
                'data': result
            }), 200

        except Exception as e:
            return jsonify({'err': str(e)}), 500

    @staticmethod
    def get_billboard_charts_score(year, week):
        if not all([year, week]):
            return jsonify({'err': 'Missing required parameters'}), 400

        try:
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

            return jsonify({
                'status': 'success',
                'data': result
            }), 200
        except Exception as e:
            return jsonify({
                'err': str(e)
            }), 500

    def calculate_music_score(country, week):
        pipeline = [
            # match country
            {"$match": {
                "country": country
            }},
            # match year
            {"$match": {
                "year": "2025"
            }},
            # match week
            {"$match": {
                "week": week
            }},
            {"$project": {
                "_id": 0,
                "datetime": "$datetime",
                "country": "$country",
                "year": "$year",
                "month": "$month",
                "day": "$day",
                "week": "$week",
                "spotify_weekly_top_songs": "$weekly_top_songs",
            }},
            {"$unwind": "$spotify_weekly_top_songs"},
            # calculate spotify score
            {"$project": {
                "datetime": "$datetime",
                "year": "$year",
                "month": "$month",
                "day": "$day",
                "week": "$week",
                "country": "$country",
                "sp_rank": {"$toInt": "$spotify_weekly_top_songs.rank"},
                # check song title
                "sp_song": "$spotify_weekly_top_songs.title",
                "sp_artist_id": "$spotify_weekly_top_songs.artist_id",
                "artist": {
                    "$trim": {
                        "input": "$spotify_weekly_top_songs.artist",
                        "chars": ","
                    }
                }
            }},
            {"$addFields": {
                "sp_score": {
                    "$subtract": [
                        {"$toInt": 201},
                        {"$toInt": "$sp_rank"}
                    ]
                }
            }},
            # group by artist, get total score
            {"$group": {
                "_id": "$sp_artist_id",
                "datetime": {"$first": "$datetime"},
                "year": {"$first": "$year"},
                "month": {"$first": "$month"},
                "day": {"$first": "$day"},
                "week": {"$first": "$week"},
                "country": {"$first": "$country"},
                "artist": {"$first": "$artist"},
                "sp_score_list": {"$addToSet": "$sp_score"}
            }},
            {"$project": {
                "sp_id": "$_id",
                "datetime": "$datetime",
                "year": "$year",
                "month": "$month",
                "day": "$day",
                "week": "$week",
                "country": "$country",
                "artist": "$artist",
                "sp_total_score": {
                    "$reduce": {
                        "input": "$sp_score_list",
                        "initialValue": 0,
                        "in": {"$add": [{"$toInt": "$$value"}, "$$this"]}
                    }
                }
            }},
            # lookup artist
            {"$lookup": {
                "from": "artist",
                "localField": "spotify_id",
                "foreignField": "sp_id",
                "as": "artist_info"
            }},
            # return needed fields
            {"$project": {
                "sp_id": "$sp_id",
                "datetime": "$datetime",
                "year": "$year",
                "month": "$month",
                "day": "$day",
                "week": "$week",
                "country": "$country",
                "artist": "$artist",
                "sp_total_score": "$sp_total_score",
                "artist_mid": {
                    "$arrayElemAt": ["$artist_info.spotify_id", 0]
                },
                "youtube_id": {
                    "$arrayElemAt": ["$artist_info.youtube_id", 0]
                }
            }},
            # lookup youtube charts
            {"$lookup": {
                "from": "youtube_charts",
                "localField": "week",
                "foreignField": "week",
                "as": "youtube_charts"
            }},
            {"$unwind": "$youtube_charts"},
            {"$match": {
                "youtube_charts.country": "south-korea"
            }},
            {"$project": {
                "mid": "$mid",
                "artist": "$artist",
                "datetime": "$datetime",
                "year": "$year",
                "month": "$month",
                "day": "$day",
                "week": "$week",
                "country": "$country",
                "sp_total_score": "$sp_total_score",
                "platforms": "$platforms",
                "youtube_week": "$youtube_charts.week",
                "youtube_country": "$youtube_charts.country",
                "youtube_charts": "$youtube_charts.weekly_top_songs"
            }},
            # convert yt_rank to integer
            {"$project": {
                "_id": 0,
                "mid": "$mid",
                "artist": "$artist",
                "datetime": "$datetime",
                "year": "$year",
                "month": "$month",
                "day": "$day",
                "week": "$week",
                "country": "$country",
                "sp_total_score": "$sp_total_score",
                "platforms": "$platforms",
                "youtube_week": "$youtube_week",
                "youtube_country": "$youtube_country",
                "yt_charts": {
                    "$map": {
                        "input": "$youtube_charts",
                        "as": "yt_item",
                        "in": {
                            "rank": {"$toInt": "$$yt_item.rank"},
                            "pre_rank": {"$toInt": "$$yt_item.previous_rank"},
                            "title": "$$yt_item.title",
                            "artist": "$$yt_item.artist",
                            "rank_position": "$$yt_item.rank_position"
                        }
                    }
                }
            }},
            # calculate youtube charts score by artists first
            {"$addFields": {
                "yt_charts": {
                    "$map": {
                        "input": "$yt_charts",
                        "as": "yt_chart",
                        "in": {
                            "$mergeObjects": [
                                "$$yt_chart",
                                {"yt_score": {
                                    "$subtract": [
                                        {"$toInt": 101},
                                        {"$toInt": "$$yt_chart.rank"}]
                                }}
                            ]
                        }
                    }
                }
            }},
            {"$unwind": "$yt_charts"},
            # return expand yt
            {"$project": {
                "mid": "$mid",
                "artist": "$artist",
                "datetime": "$datetime",
                "year": "$year",
                "month": "$month",
                "day": "$day",
                "week": "$week",
                "country": "$country",
                "sp_total_score": "$sp_total_score",
                "platforms": "$platforms",
                "youtube_week": "$youtube_week",
                "youtube_country": "$youtube_country",
                "yt_charts_artist": "$yt_charts.artist",
                "yt_score": "$yt_charts.yt_score"
            }},
            {"$group": {
                "_id": "$yt_charts_artist",
                "_all": {"$addToSet": "$$ROOT"},
                "yt_score_list": {"$addToSet": "$yt_score"},
                "yt_artist": {"$first": "$yt_charts_artist"}
            }},
            # calculate yt total score
            {"$project": {
                "_id": 0,
                "_all": "$_all",
                "yt_artist": "$yt_artist",
                "yt_total_score": {
                    "$reduce": {
                        "input": "$yt_score_list",
                        "initialValue": 0,
                        "in": {
                            "$add": [{"$toInt": "$$value"}, "$$this"]
                        }
                    }
                }
            }},
            # match yt_artist with sp_artist,
            # if artist name is the same, keep it; not the same, drop it
            {"$addFields": {
                "_artist": {
                    "$filter": {
                        "input": "$_all",
                        "cond": {
                            "$eq": ["$$this.artist", "$$this.yt_charts_artist"]
                        }
                    }
                }
            }},
            {"$project": {
                "yt_artist": "$yt_artist",
                "yt_total_score": "$yt_total_score",
                "artist": {
                    "$arrayElemAt": ["$_artist", 0]
                }
            }},
            # organize artist info
            {"$project": {
                "mid": "$artist.mid",
                "artist": "$artist.artist",
                "year": {"$toInt": "$artist.year"},
                "week": "$artist.week",
                "country": "$youtube_country",
                "spotify_total_score": "$artist.sp_total_score",
                "youtube_total_score": "$artist.yt_score",
                "platforms": "$artist.platforms"
            }},
            # lookup billboard global 200
            {"$lookup": {
                "from": "billboard_charts",
                "localField": "week",
                "foreignField": "week",
                "as": "billboard_charts"
            }},
            # billboard ranking is global ranking
            {"$project": {
                "artist": "$artist",
                "year": "$year",
                "week": "$week",
                "spotify_total_score": "$spotify_total_score",
                "youtube_total_score": "$youtube_total_score",
                "billboard_charts": {
                    "$arrayElemAt": ["$billboard_charts.data", 0]
                }
            }},
            # convert billboard rank to integer
            {"$project": {
                "artist": "$artist",
                "year": "$year",
                "week": "$week",
                "spotify_total_score": "$spotify_total_score",
                "youtube_total_score": "$youtube_total_score",
                "bb_charts": {
                    "$map": {
                        "input": "$billboard_charts",
                        "as": "bb_item",
                        "in": {
                            "rank": {"$toInt": "$$bb_item.ranking"},
                            "artist": "$$bb_item.artist"
                        }
                    }
                }
            }},
            # calculate billboard charts score
            {"$addFields": {
                "bb_charts": {
                    "$map": {
                        "input": "$bb_charts",
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
            {"$unwind": "$bb_charts"},
            # return expanded billboard
            {"$project": {
                "artist": "$artist",
                "year": "$year",
                "week": "$week",
                "spotify_total_score": "$spotify_total_score",
                "youtube_total_score": "$youtube_total_score",
                "bb_charts_artist": "$bb_charts.artist",
                "bb_score": "$bb_charts.bb_score"
            }},
            {"$group": {
                "_id": "$bb_charts_artist",
                "_all": {"$addToSet": "$$ROOT"},
                "bb_score_list": {"$addToSet": "$bb_score"},
                "bb_artist": {"$first": "$bb_charts_artist"}
            }},
            # calculate billboard total score
            {"$project": {
                "_id": 0,
                "_all": "$_all",
                "bb_artist": "$bb_artist",
                "bb_total_score": {
                    "$reduce": {
                        "input": "$bb_score_list",
                        "initialValue": 0,
                        "in": {
                            "$add": [{"$toInt": "$$value"}, "$$this"]
                        }
                    }
                }
            }},
            # match billboard artist with artist
            # if text contains artist name, keep the value
            {"$addFields": {
                "_artist": {
                    "$filter": {
                        "input": "$_all",
                        "as": "temp",
                        "cond": {
                            "$eq": ["$$temp.artist", "$$temp.bb_charts_artist"]
                        }
                    }
                }
            }
            },
            {"$sort": {"bb_total_score": -1}},
            # match artist
            {"$project": {
                "bb_artist": "$bb_artist",
                "bb_total_score": "$bb_total_score",
                "artist": {
                    "$arrayElemAt": ["$_artist", 0]
                }
            }},
            # return needed fields
            {"$project": {
                "artist": "$artist.artist",
                "year": "$artist.year",
                "week": "$artist.week",
                "spotify_total_score": "$artist.spotify_total_score",
                "youtube_total_score": "$artist.youtube_total_score",
                "billboard_total_score": "$bb_total_score"
            }},
            {"$match": {
                "artist": {"$ne": None}
            }},
            {"$addFields": {
                "music_performance_score": {
                    "$multiply": [
                        {"$add": ["$spotify_total_score", "$youtube_total_score", "$billboard_total_score"]}, 0.3
                    ]
                }
            }},
            {"$sort": {"music_performance_score": -1}}
        ]

