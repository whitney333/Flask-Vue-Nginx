from flask import request, jsonify
import json
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

            return result
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

            return result
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

            return result
        except Exception as e:
            return jsonify({
                'err': str(e)
            }), 500

    @classmethod
    def merge_all_music_scores(self, country, year, week):
        sp_data = self.get_spotify_charts_score(country, year, week)
        yt_data = self.get_youtube_charts_score(country, year, week)
        bb_data = self.get_billboard_charts_score(year, week)

        merged_data = []

        # Step 1: Merge yt_data with sp_data and bb_data
        for yt_artist in yt_data:
            merged_artist = yt_artist.copy()  # Start with YouTube data

            # Check for match in sp_data
            sp_match = next((sp for sp in sp_data if sp['artist'] == yt_artist['artist']), None)
            if sp_match:
                merged_artist.update(sp_match)  # Merge Spotify data

            # Check for match in bb_data
            bb_match = next((bb for bb in bb_data if bb['artist'] == yt_artist['artist']), None)
            if bb_match:
                merged_artist.update(bb_match)  # Merge Billboard data

            merged_data.append(merged_artist)

        # Step 2: Add unmatched sp_data artists
        for sp_artist in sp_data:
            if not any(artist['artist'] == sp_artist['artist'] for artist in merged_data):
                merged_data.append(sp_artist)

        # Step 3: Add unmatched bb_data artists
        for bb_artist in bb_data:
            if not any(artist['artist'] == bb_artist['artist'] for artist in merged_data):
                merged_data.append(bb_artist)
        print(merged_data)
        return merged_data

    @staticmethod
    def calculate_total_music_score(merge_list):
        # Calculate total_score for each artist
        for item in merge_list:
            youtube_score = item.get('youtube_score', 0)
            billboard_score = item.get('billboard_score', 0)
            spotify_score = item.get('sp_total_score', 0)
            item['total_score'] = youtube_score + billboard_score + spotify_score

        # Sort by total_score in descending order
        sorted_list = sorted(merge_list, key=lambda x: x['total_score'], reverse=True)

        return sorted_list

    @classmethod
    def get_music_score(cls, country, year, week):
        # TODO Add spotify monthly listeners index of every artist
        ## in order to avoid artists that do not enter the charts
        if not all([country, year, week]):
            return jsonify({'err': 'Missing required parameters'}), 400

        try:
            merge_list = cls.merge_all_music_scores(country, year, week)
            results = cls.calculate_total_music_score(merge_list)

            return jsonify({
                'status': 'success',
                'data': results
            }), 200
        except Exception as e:
            return jsonify({
                'err': str(e)
            }), 500

    @classmethod
    def get_drama_score(cls):
        pass
