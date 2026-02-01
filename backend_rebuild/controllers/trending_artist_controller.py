from flask import request, jsonify
import json
import re
import pandas as pd
from copy import deepcopy
from collections import defaultdict
from models.artist_model import Artists
# music related data
from models.spotify_model import SpotifyCharts, SpotifyOst, Spotify
from models.sns.youtube_model import YoutubeCharts
from models.billboard_model import BillboardCharts
# sns related data
from models.sns.youtube_model import Youtube
from models.sns.instagram_model import Instagram, InstagramLatest
from models.sns.tiktok_model import Tiktok
# drama related data
from models.netflix_model import NetflixCharts
from models.drama_model import Drama


class TrendingArtistController:
    """
    Calculate Trending Artist Score from 3 aspects:
    1) Music Performance
        Includes: Spotify_Charts, Youtube_Charts, Billboard_Charts
    2) SNS Performance
        Includes: Instagram, Tiktok, YouTube
    3) Drama Performance
        Includes: Netflix_Charts, Spotify_Ost
    """
    @staticmethod
    def query_db_artist():
        """
        Get all artists' name, social media IDs, and music platform IDs
        :return:
        """
        pipeline = [
            {"$match": {
                "artist_id": {"$ne": None}
            }},
            {"$project": {
                "_id": 0,
                "artist_id": "$artist_id",
                "type": "$type",
                "artist": "$english_name",
                "korean_name": "$korean_name",
                "instagram_id": "$instagram_id",
                "instagram_user": "$instagram_user",
                "youtube_id": "$youtube_id",
                "tiktok_id": "$tiktok_id",
                "spotify_id": "$spotify_id"
            }}
        ]

        artists = Artists.objects().aggregate(pipeline)
        result = list(artists)

        return result

    @staticmethod
    def get_spotify_popularity(spotify_id):
        """
        To avoid artists do not enter any music charts,
        we add spotify popularity index as the base score
        :return:
        """
        # Validate required parameters
        if not spotify_id:
            return jsonify({'err': 'Missing artist_id parameter'}), 400

        # get the latest popularity index
        pipeline = [
            {"$match": {
                "spotify_id": spotify_id
            }},
            {"$sort": {"datetime": -1}},
            {"$limit": 1},
            {"$project": {
                "_id": 0,
                "spotify_id": "$spotify_id",
                "popularity": "$popularity"
            }}
        ]

        results = Spotify.objects().aggregate(pipeline)
        result = list(results)

        return result

    @classmethod
    def get_spotify_popularity_score(cls):
        # get all artists in db
        artists = cls.query_db_artist()

        combined_spotify_score = []

        for artist in artists:
            merged_artist = artist.copy()
            if merged_artist.get("spotify_id"):
                spotify_popularity = cls.get_spotify_popularity(artist.get("spotify_id"))
                merged_artist["sp_pop_score"] = spotify_popularity[0]["popularity"]
            combined_spotify_score.append(merged_artist)

        return combined_spotify_score

    @staticmethod
    def get_spotify_charts_score(country, year, week):
        # Validate required parameters
        if not country:
            return jsonify({'err': 'Missing country parameter'}), 400
        if not year:
            return jsonify({'err': 'Missing year parameter'}), 400
        if not week:
            return jsonify({'err': 'Missing week parameter'}), 400

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
                "spotify_id": "$_id",
                "datetime": "$datetime",
                "year": "$year",
                "month": "$month",
                "day": "$day",
                "week": "$week",
                "country": "$country",
                "artist": "$artist",
                "sp_chart_score": {
                    "$reduce": {
                        "input": "$sp_score_list",
                        "initialValue": 0,
                        "in": {"$add": [{"$toInt": "$$value"}, "$$this"]}
                    }
                }
            }},
            {"$sort": {"sp_chart_score": -1}},
            # # lookup artist
            # {"$lookup": {
            #     "from": "artists",
            #     "localField": "sp_id",
            #     "foreignField": "spotify_id",
            #     "as": "artist_info"
            # }},
            # # unwind artist_info field and simultaneously keep other records which do not have this field
            # {"$unwind": {
            #     "path": "$artist_info",
            #     "preserveNullAndEmptyArrays": True
            # }},
            # # keep artist id from all platforms
            # {"$project": {
            #     "_id": 0,
            #     "datetime": "$datetime",
            #     "year": "$year",
            #     "month": "$month",
            #     "day": "$day",
            #     "week": "$week",
            #     "country": "$country",
            #     "artist": "$artist",
            #     "type": "$artist_info.type",
            #     "mid": "$artist_info.artist_id",
            #     "sp_chart_score": "$sp_total_score",
            #     "spotify_id": "$sp_id",
            #     "instagram_id": "$artist_info.instagram_id",
            #     "instagram_user": "$artist_info.instagram_user",
            #     "youtube_id": "$artist_info.youtube_id",
            #     "tiktok_id": "$artist_info.tiktok_id"
            # }}
        ]

            results = SpotifyCharts.objects().aggregate(pipeline)

            result = []
            for item in results:
                result.append(item)

            return result
        except Exception as e:
            return jsonify({'err': str(e)}), 500

    @classmethod
    def merge_spotify_score(cls, country, year, week):
        # Validate required parameters
        if not country:
            return jsonify({'err': 'Missing country parameter'}), 400
        if not year:
            return jsonify({'err': 'Missing year parameter'}), 400
        if not week:
            return jsonify({'err': 'Missing week parameter'}), 400

        try:
            sp_chart = cls.get_spotify_charts_score(country, year, week)
            sp_pop = cls.get_spotify_popularity_score()

            merged_list = []
            for chart_item in sp_chart:
                #  find matching in spotify popularity
                pop_match = next(
                    (pop_item for pop_item in sp_pop if pop_item["spotify_id"] == chart_item["spotify_id"]),
                    None
                )
                if pop_match:
                    # Merge dictionaries (sp_chart fields take precedence in case of conflict)
                    sp_total_score = pop_match["sp_pop_score"] + chart_item["sp_chart_score"]

                    merged_item = {
                        # **pop_match, **chart_item,
                        "artist": pop_match["artist"],
                        "korean_name": pop_match["korean_name"],
                        "mid": pop_match["artist_id"],
                        "type": pop_match["type"],
                        "country": chart_item["country"],
                        "year": chart_item["year"],
                        "month": chart_item["month"],
                        "day": chart_item["day"],
                        "week": chart_item["week"],
                        "datetime": chart_item["datetime"],
                        "instagram_id": pop_match["instagram_id"],
                        "instagram_user": pop_match["instagram_user"],
                        "spotify_id": pop_match["spotify_id"],
                        "tiktok_id": pop_match["tiktok_id"],
                        "youtube_id": pop_match["youtube_id"],
                        "spotify_score": sp_total_score
                    }
                    merged_list.append(merged_item)
                else:
                    merged_list.append(chart_item)

            # Step 2: Add sp_pop items that weren't in sp_chart
            sp_pop_ids_in_chart = {item["spotify_id"] for item in sp_chart}
            unmatched_pop_items = [
                pop_item for pop_item in sp_pop
                if pop_item["spotify_id"] not in sp_pop_ids_in_chart
            ]

            final_merged = merged_list + unmatched_pop_items

            results = []
            # check if total score not exists,count chart score or popularity score
            for item in final_merged:
                # Create a new dict without sp_chart_score and sp_pop_score
                new_item = {k: v for k, v in item.items() if k not in ["sp_chart_score", "sp_pop_score"]}

                if "spotify_score" in item:
                    # artist already has total_score
                    pass
                elif "sp_chart_score" in item:
                    new_item["spotify_score"] = item["sp_chart_score"]
                elif "sp_pop_score" in item:
                    new_item["spotify_score"] = item["sp_pop_score"]
                else:
                    # skip if no score exists
                    continue
                results.append(new_item)

            # return only items that have sp_total_score
            final_result = [item for item in results if 'spotify_score' in item]

            # Sorted results by spotify_score in descending
            sorted_result = sorted(final_result, key=lambda x: x["spotify_score"], reverse=True)

            # Limit 100 results
            top_result = sorted_result[:100]

            return top_result
        except Exception as e:
            return jsonify({
                'status': 'error',
                'err': str(e)
            })

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
    def merge_music_scores(cls, country, year, week):
        # music data
        sp_data = cls.merge_spotify_score(country, year, week)
        yt_data = cls.get_youtube_charts_score(country, year, week)
        bb_data = cls.get_billboard_charts_score(year, week)

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

        # print(merged_data)
        return merged_data

    @classmethod
    def get_music_score(cls, country, year, week):
        # Validate required parameters
        if not country:
            return jsonify({'err': 'Missing country parameter'}), 400
        if not year:
            return jsonify({'err': 'Missing year parameter'}), 400
        if not week:
            return jsonify({'err': 'Missing week parameter'}), 400

        try:
            merge_list = cls.merge_music_scores(country, year, week)
            total_music_score = cls.calculate_total_music_score(merge_list)

            # Return artist info & total_music_score fields
            filtered_results = []
            for item in total_music_score:
                filtered_item = {key: value for key, value in item.items()
                                 if key not in ['spotify_score', 'billboard_score', 'youtube_score']}
                filtered_results.append(filtered_item)

            return filtered_results
        except Exception as e:
            return jsonify({
                'status': 'error',
                'err': str(e)
            }), 500

    @classmethod
    def merge_all_sns_scores(self, country, year, week):
        """
        Based on music scores, add on sns_score
        :param country:
        :param year:
        :param week:
        :return:
        """
        merge_music_data = self.merge_music_scores(country, year, week)

        concat_sns_list = []

        # lookup artist in youtube collection
        for artist in merge_music_data:
            merged_artist = artist.copy()

            # match youtube_sns_score
            if merged_artist.get("youtube_id"):
                yt_sns_scores = self.get_youtube_score(merged_artist.get("youtube_id"))
                merged_artist["youtube_sns_score"] = yt_sns_scores[0]["hashtag"]
            else:
                merged_artist["youtube_sns_score"] = 0
            # match tiktok_sns_score
            if merged_artist.get("tiktok_id"):
                tk_sns_scores = self.get_tiktok_score(merged_artist.get("tiktok_id"))
                merged_artist["tiktok_sns_score"] = tk_sns_scores[0]["hashtag"]
            else:
                merged_artist["tiktok_sns_score"] = 0
            # match instagram_sns_score
            # if merged_artist.get("instagram_id"):
            #     ig_sns_scores = self.get_instagram_score(merged_artist.get("instagram_id"))
            #     merged_artist["instagram_sns_score"] = ig_sns_scores
            # else:
            #     merged_artist["instagram_sns_score"] = 0

            concat_sns_list.append(merged_artist)

        print(concat_sns_list)
        return concat_sns_list

    @staticmethod
    def calculate_total_music_score(merge_list):
        # Calculate total_score for each artist
        for item in merge_list:
            # Calculate music score
            youtube_score = item.get('youtube_score', 0)
            billboard_score = item.get('billboard_score', 0)
            spotify_score = item.get('spotify_score', 0)
            item['total_music_score'] = youtube_score + billboard_score + spotify_score
            # Calculate sns score
            # youtube_sns_score = item.get('youtube_sns_score', 0)
            # tiktok_sns_score = item.get('tiktok_sns_score', 0)
            # instagram_sns_score = item.get('instagram_sns_score', 0)
            # item['total_sns_score'] = youtube_sns_score + tiktok_sns_score + instagram_sns_score

        # Sort by total_score in descending order
        sorted_list = sorted(merge_list, key=lambda x: x['total_music_score'], reverse=True)

        # Limit 100
        top_result = sorted_list[:100]

        return top_result


    ### Drama Score Section ###
    @classmethod
    def get_netflix_chart(cls, country, year, week):
        # Validate required parameters
        if not country:
            return jsonify({'err': 'Missing country parameter'}), 400
        if not year:
            return jsonify({'err': 'Missing year parameter'}), 400
        if not week:
            return jsonify({'err': 'Missing week parameter'}), 400

        try:
            pipeline = [
                {"$match": {
                    "country": country
                }},
                {"$project": {
                    "_id": 0,
                    "datetime": "$datetime",
                    "week": "$week",
                    "country": "$country",
                    "rank": "$rank",
                    "name": "$name",
                    "weeks_on_chart": "$weeks_on_chart"
                }},
                {"$addFields": {
                    "year": {
                        "$year": "$datetime"
                    }
                }},
                # match year & week
                {"$match": {
                    "year": int(year),
                    "week": int(week)
                }},
                # # calculate rank score
                {"$addFields": {
                    "rank_score": {
                        "$subtract": [201, {"$toInt": "$rank"}]}
                }},
                {"$project": {
                    "_id": 0,
                    "year": "$year",
                    "week": "$week",
                    "country": "$country",
                    "rank": "$rank",
                    "netflix_score": {"$toInt": "$rank_score"},
                    "name": "$name",
                    "weeks_on_chart": "$weeks_on_chart"
                }}
            ]
            results = NetflixCharts.objects().aggregate(pipeline)
            result = list(results)

            return result
        except Exception as e:
            return jsonify({
                'status': 'error',
                'err': str(e)
            }), 500

    @classmethod
    def get_spotify_ost(cls, year, week):
        # Validate required parameters
        if not year:
            return jsonify({'err': 'Missing year parameter'}), 400
        if not week:
            return jsonify({'err': 'Missing week parameter'}), 400

        try:
            year = int(year)
            pipeline = [
                {"$match": {
                    "year": year,
                    "week": week
                }},
                {"$project": {
                    "_id": 0,
                    "year": "$year",
                    "week": "$week",
                    "datetime": "$datetime",
                    "track": "$track",
                    "track_code": "$track_code",
                    "album": "$album",
                    "album_code": "$album_code",
                    "artist": "$artist",
                    "artist_code": "$artist_code",
                    "added_at": "$added_at",
                    "country": "$country",
                    "release_date": "$release_date",
                    "popularity": "$popularity",
                    "thumbnail": "$thumbnail",
                    "play_counts": {"$toInt": "$play_counts"}
                }}
                # {"$match": {
                #     "BROADCAST_YEAR": {
                #         "$gte": year - 1,
                #         "$lte": year
                #     }
                # }},
                # {"$project": {
                #     "english_name": "$NAME",
                #     "korean_name": "$NAME_IN_KOREAN",
                #     "artist_id": "$STARRING.MID"
                # }},
                # # lookup spotify ost
                # {"$lookup": {
                #     "from": "spotify_ost",
                #     "let": {"english_name": "$english_name"},
                #     "pipeline": [
                #         {"$match": {
                #             "year": year,
                #             "week": week
                #         }}
                #     ],
                #     "as": "spotify_ost"
                # }},
                # {"$unwind": "$spotify_ost"},
                # # match drama name with album name
                # {"$addFields": {
                #     "is_match": {
                #         "$regexMatch": {
                #             "input": "$spotify_ost.album",
                #             "regex": {
                #                 "$concat": [".*", {"$toString": "$english_name"}, ".*"]
                #             },
                #             "options": "i"
                #         }
                #     }
                # }},
                # # return matched drama
                # {"$match": {
                #     "is_match": True
                # }},
                # # group by drama
                # {"$group": {
                #     "_id": "$english_name",
                #     "korean_name": {"$first": "$korean_name"},
                #     "artist_id": {"$first": "$artist_id"},
                #     "year": {"$first": "$spotify_ost.year"},
                #     "week": {"$first": "$spotify_ost.week"},
                #     "play_counts": {"$push": {"$toInt": "$spotify_ost.play_counts"}}
                # }},
                # # return sum up play_counts
                # {"$project": {
                #     "_id": 0,
                #     "english_name": "$_id",
                #     "korean_name": "$korean_name",
                #     "artist_id": "$artist_id",
                #     "year": "$year",
                #     "week": "$week",
                #     "play_counts": {"$sum": "$play_counts"}
                # }},
                # {"$unwind": "$artist_id"},
                # {"$group": {
                #     "_id": "$artist_id",
                #     "english_name": {"$push": "$english_name"},
                #     "korean_name": {"$push": "$korean_name"},
                #     "year": {"$first": "$year"},
                #     "week": {"$first": "$week"},
                #     "ost_score": {"$push": "$play_counts"}
                # }}
            ]

            results = SpotifyOst.objects().aggregate(pipeline)
            result = list(results)

            return result
        except Exception as e:
            return jsonify({
                'status': 'error',
                'err': str(e)
            }), 500

    @staticmethod
    def get_dramas(year):
        # Validate required parameters
        if not year:
            return jsonify({'err': 'Missing year parameter'}), 400

        try:

            year = int(year)
            pipeline = [
                {"$match": {
                    "BROADCAST_YEAR": {
                        "$gte": year - 1,  # fetch drama within 2 yrs
                        "$lte": year
                    }
                }},
                {"$project": {
                    "_id": 0,
                    "english_name": "$NAME",
                    "korean_name": "$NAME_IN_KOREAN",
                    "artist_id": "$STARRING.MID"
                }},
            ]

            results = Drama.objects().aggregate(pipeline)
            result = list(results)

            return result
        except Exception as e:
            return jsonify({
                'status': 'error',
                'err': str(e)
            }), 500

    @staticmethod
    def extract_base_title(title):
        """
        To extract base title using regex
        :param title:
        :return:
        """
        # Remove ": Limited Series", ": Season X" and similar suffixes
        match = re.match(r'^(.*?)(?:\s*:\s*(?:Limited Series|Season\s*\d+))?$', title)

        return match.group(1).strip() if match else title

    @staticmethod
    def match_ost_with_drama(ost, drama):
        """
        match album names with Korean drama names using regex
        :param ost <list>
        :param drama <list>
        :return:
        """
        # Validate required parameters
        if not ost:
            return jsonify({'err': 'Missing ost parameter'}), 400
        if not drama:
            return jsonify({'err': 'Missing drama parameter'}), 400

        try:
            matched = []
            for song in ost:
                album_name = song['album']
                matched_dramas = []
                for d in drama:
                    english_name = d['english_name']
                    artist_id = d['artist_id']
                    # Create a regex pattern to find the English name in the album name with .* before and after
                    pattern = f".*{re.escape(english_name)}.*"
                    if re.search(pattern, album_name):
                        matched_dramas.append({
                            'english_name': d['english_name'],
                            'artist_id': d['artist_id']
                        })
                if matched_dramas:
                    song_info = {
                        'track': song['track'],
                        'album': song['album'],
                        'play_counts': song['play_counts'],
                        'matched_names': matched_dramas[0]['english_name'],
                        'artist_id': matched_dramas[0]['artist_id']
                    }
                    matched.append(song_info)
            return matched
        except Exception as e:
            return jsonify({
                'status': 'error',
                'err': str(e)
            })

    @classmethod
    def filter_ost_by_drama_name(cls, year, week):
        # Validate required parameters
        if not year:
            return jsonify({'err': 'Missing year parameter'}), 400
        if not week:
            return jsonify({'err': 'Missing week parameter'}), 400

        ost = cls.get_spotify_ost(year, week)
        drama = cls.get_dramas(year)

        # Get the matched results
        result = cls.match_ost_with_drama(ost, drama)

        # Create a dictionary to store summed play counts and artist_ids
        summed_data = defaultdict(lambda: {"total_plays": 0, "artist_id": None})

        for entry in result:
            name = entry["matched_names"]
            summed_data[name]["total_plays"] += int(entry["play_counts"])
            summed_data[name]["artist_id"] = entry["artist_id"]  # Will keep the last artist_id found

        # Convert to final result format
        final_result = [
            {
                "english_name": name,
                "ost_score": int(data["total_plays"]),
                "artist_id": data["artist_id"]
            }
            for name, data in summed_data.items()
        ]

        return final_result

    @classmethod
    def merge_drama_score(cls, country, year, week):
        """
        Merge OST Score with Netflix score
        :param country:
        :param year:
        :param week:
        :return: list
        """
        # Validate required parameters
        if not country:
            return jsonify({'err': 'Missing country parameter'}), 400
        if not year:
            return jsonify({'err': 'Missing year parameter'}), 400
        if not week:
            return jsonify({'err': 'Missing week parameter'}), 400

        # get spotify ost list
        ost = cls.filter_ost_by_drama_name(year, week)
        # get netflix chart
        netflix = cls.get_netflix_chart(country, year, week)
        # Create a dictionary for OST data for easier lookup
        ost_dict = {item['english_name']: item for item in ost}

        merged = []

        # Process Netflix items
        for netflix_item in netflix:
            # Extract base name by removing the subtitle (everything after colon)
            base_name = netflix_item['name'].split(':')[0].strip()
            merged_item = netflix_item.copy()

            # Try to find matching OST entry
            matched_ost = None
            for ost_name, ost_item in ost_dict.items():
                if ost_name.lower() in netflix_item['name'].lower() or base_name.lower() in ost_name.lower():
                    matched_ost = ost_item
                    break

            if matched_ost:
                # Merge the data
                merged_item.update({
                    'artist_id': matched_ost['artist_id'],
                    'ost_score': matched_ost['ost_score'],
                    'drama_score': matched_ost['ost_score'] + netflix_item['netflix_score']
                })
            else:
                # Only Netflix data available
                merged_item['drama_score'] = netflix_item['netflix_score']

            merged.append(merged_item)

        # Add OST items that weren't in Netflix
        for ost_item in ost:
            found = False
            for netflix_item in netflix:
                base_name = netflix_item['name'].split(':')[0].strip()
                if ost_item['english_name'].lower() in netflix_item['name'].lower() or base_name.lower() in ost_item[
                    'english_name'].lower():
                    found = True
                    break

            if not found:
                merged.append({
                    'artist_id': ost_item['artist_id'],
                    'english_name': ost_item['english_name'],
                    'ost_score': ost_item['ost_score'],
                    'netflix_score': 0,
                    'drama_score': ost_item['ost_score']
                })

        return merged

    @staticmethod
    def get_db_artist_ids(artist_id):
        """
         Get all artists' name, social media IDs, and music platform IDs
         :return:
         """
        if not all([artist_id]):
            return jsonify({'err': 'Missing required parameters'}), 400

        pipeline = [
            {"$match": {
                "artist_id": artist_id
            }},
            {"$project": {
                "_id": 0,
                "artist_id": "$artist_id",
                "type": "$type",
                "nation": "$nation",
                "artist": "$english_name",
                "korean_name": "$korean_name",
                "instagram_id": "$instagram_id",
                "youtube_id": "$youtube_id",
                "tiktok_id": "$tiktok_id",
                "spotify_id": "$spotify_id",
                "image_url": "$image_url"
            }}
        ]

        artists = Artists.objects().aggregate(pipeline)
        results = []
        for artist in artists:
            results.append(artist)

        return results

    @classmethod
    def get_drama_score(cls, country, year, week):
        merged_drama = cls.get_pre_drama_score(country, year, week)

        try:
            combined_list = []

            for drama in merged_drama:
                _merged = drama.copy()
                if drama.get("artist_id"):
                    artist_ids = cls.get_db_artist_ids(_merged.get("artist_id"))
                    # print(type(artist_ids))
                    # _merged["_"] = artist_ids

                    # check if _ field has element
                    if len(artist_ids) == 1:
                        _merged["name"] = artist_ids[0]["artist"]
                        _merged["instagram_id"] = artist_ids[0]["instagram_id"]
                        _merged["youtube_id"] = artist_ids[0]["youtube_id"]
                        _merged["tiktok_id"] = artist_ids[0]["tiktok_id"]
                        _merged["type"] = artist_ids[0]["type"]

                        combined_list.append(_merged)
            # print(combined_list)

            return combined_list
        except Exception as e:
            return jsonify({
                'err': str(e)
            }), 500

    @staticmethod
    def calculate_total_drama_score(merge_list):
        # Calculate total_score for each artist
        for item in merge_list:
            netflix_score = item.get('netflix_score', 0)
            ost_score = item.get('ost_score', 0)
            item['total_drama_score'] = netflix_score + ost_score

        # Sort by total_score in descending order
        sorted_list = sorted(merge_list, key=lambda x: x['total_drama_score'], reverse=True)

        return sorted_list

    @classmethod
    def get_pre_drama_score(cls, country, year, week):
        # Validate required parameters
        if not country:
            return jsonify({'err': 'Missing country parameter'}), 400
        if not year:
            return jsonify({'err': 'Missing year parameter'}), 400
        if not week:
            return jsonify({'err': 'Missing week parameter'}), 400

        try:
            merge_list = cls.merge_drama_score(country, year, week)
            result = cls.calculate_total_drama_score(merge_list)

            # Create a dictionary to aggregate data by artist_id
            artist_dict = {}

            for item in result:
                if "artist_id" not in item:
                    continue

                english_name = item.get("english_name") or item.get("name")

                for artist_id in item["artist_id"]:
                    if artist_id not in artist_dict:
                        artist_dict[artist_id] = {
                            "artist_id": artist_id,
                            "english_name": [],
                            "total_drama_score": 0
                        }

                    if english_name:
                        artist_dict[artist_id]["english_name"].append(english_name)
                    artist_dict[artist_id]["total_drama_score"] += item.get("total_drama_score", 0)

            # Convert the dictionary to a list of values
            final_result = list(artist_dict.values())
            # Sort result in descending order
            sorted_list = sorted(final_result, key=lambda x: x['total_drama_score'], reverse=True)
            # Limit 100
            top_result = sorted_list[:100]

            return top_result
        except Exception as e:
            return jsonify({
                'status': 'error',
                'err': str(e)
            })

    ### SNS Score Section ###
    @staticmethod
    def get_instagram_7day_follower_growth(artist_id):
        if not artist_id:
            return jsonify({'err': 'Missing artist_id parameter'}), 400

        try:
            pipeline = [
                {"$match": {
                        "user_id": artist_id
                }},
                {"$sort": {"datetime": -1}},
                {"$limit": 7},
                {"$group": {
                    "_id": "$user_id",
                    "firstRecord": { "$first": "$$ROOT"},
                    "lastRecord": { "$last": "$$ROOT"},
                    "records": { "$push": "$$ROOT"}
                }},
                {"$project": {
                    "_id": 1,
                    "growth_score": {
                        "$subtract": [
                            "$firstRecord.follower_count", "$lastRecord.follower_count"
                        ]
                    }
                }}
            ]

            results = Instagram.objects().aggregate(pipeline)
            result = list(results)

            return result
        except Exception as e:
            return jsonify({
                'status': 'error',
                'err': str(e)
            }), 500

    @staticmethod
    def get_instagram_engage(artist_id):
        if not artist_id:
            return jsonify({'err': 'Missing artist_id parameter'}), 400

        try:
            pipeline = [
                {"$match": {
                    "user_id": artist_id
                }},
                {"$sort": {"datetime": -1}},
                {"$limit": 1},
                {"$unwind": "$posts"},
                # calculate engagement by sum up: like_count & comment_count
                {"$project": {
                    "_id": 0,
                    "datetime": "$datetime",
                    "user_id": "$user_id",
                    "engagement": {
                        "$sum": ["$posts.like_count", "$posts.comment_count"]
                    }
                }},
                # group by artist
                {"$group": {
                    "_id": "$user_id",
                    "user_id": {"$first": "$user_id"},
                    "datetime": {"$first": "$datetime"},
                    "engagement_score": {"$sum": "$engagement"}
                }}
            ]

            results = InstagramLatest.objects().aggregate(pipeline)
            result = list(results)

            return result
        except Exception as e:
            return jsonify({
                'status': 'error',
                'err': str(e)
            }), 500

    @classmethod
    def get_instagram_score(cls, artist_id):
        """
        Get Instagram latest 12 posts' total likes & comments,
        and 7-day follower growth
        :parameter: instagram_id
        :return:
        """

        follower_growth = cls.get_instagram_7day_follower_growth(artist_id)
        engagement = cls.get_instagram_engage(artist_id)

        # Check if list is null
        if len(follower_growth) == 1:
            growth_score = follower_growth[0]["growth_score"]
        else:
            growth_score = 0

        if len(engagement) == 1:
            engage_score = engagement[0]["engagement_score"]
        else:
            engage_score = 0

        # instagram_score = int(follower_growth_score[0]) + int(engagement_score[0])
        # print(instagram_score)
        result = [{
            "growth_score": growth_score,
            "engagement_score": engage_score,
            "instagram_score": growth_score + engage_score
        }]
        # print(type(follower_growth))
        # print(type(engagement))

        return result

    @staticmethod
    def get_youtube_score(artist_id):
        """
        Based on music merged_list, add on each artist's youtube sns score
        :param artist_id:
        :return:
        """
        if not all([artist_id]):
            return jsonify({'err': 'Missing required parameters'}), 400

        try:
            pipeline = [
                {"$match": {
                    "channel_id": artist_id
                }},
                {"$sort": {"datetime": -1}},
                {"$limit": 1},
                # return hashtag counts
                {"$project": {
                    "_id": 0,
                    "youtube_id": "$channel_id",
                    "datetime": "$datetime",
                    "hashtag": {
                        "$sum": ["$channel_hashtag", "$video_hashtag"]
                    }
                }}
            ]

            results = Youtube.objects().aggregate(pipeline)
            result = []
            for item in results:
                result.append(item)

            return result
        except Exception as e:
            return jsonify({
                'err': str(e)
            }), 500

    @staticmethod
    def get_tiktok_score(artist_id):
        if not all([artist_id]):
            return jsonify({'err': 'Missing required parameters'}), 400

        try:
            pipeline = [
                {"$match": {
                    "id": artist_id
                }},
                {"$sort": {"datetime": -1}},
                {"$limit": 1},
                {"$project": {
                    "_id": 0,
                    "tiktok_id": "$id",
                    "datetime": "$datetime",
                    "hashtag": {"$toInt": "$hashtag"}
                }}
            ]

            results = Tiktok.objects().aggregate(pipeline)
            result = []
            for item in results:
                result.append(item)

            return result
        except Exception as e:
            return jsonify({
                'err': str(e)
            }), 500

    @classmethod
    def get_artist_sns_score(self):
        # get all artists in db
        artists = self.query_db_artist()
        # print(artists)

        combined_artist_sns_score = []

        # print(type(merged_artist))
        for artist in artists:
            combined_artist = artist.copy()
            # match youtube_sns_score
            if combined_artist.get("youtube_id"):
                yt_sns_scores = self.get_youtube_score(combined_artist.get("youtube_id"))
                combined_artist["youtube_sns_score"] = yt_sns_scores[0]["hashtag"]
            else:
                combined_artist["youtube_sns_score"] = 0
            # match tiktok_sns_score
            if combined_artist.get("tiktok_id"):
                tk_sns_scores = self.get_tiktok_score(combined_artist.get("tiktok_id"))
                # if list is not null
                if len(tk_sns_scores) == 1:
                    combined_artist["tiktok_sns_score"] = tk_sns_scores[0]["hashtag"]
                else:
                    combined_artist["tiktok_sns_score"] = 0
            else:
                combined_artist["tiktok_sns_score"] = 0
            # match instagram_sns_score
            if combined_artist.get("instagram_id"):
                ig_sns_scores = self.get_instagram_score(combined_artist.get("instagram_id"))
                # print(ig_sns_scores)
                # if list is not null
                if len(ig_sns_scores) == 1:
                    combined_artist["instagram_sns_score"] = ig_sns_scores[0]["instagram_score"]
                    # print(type(ig_sns_scores))
                else:
                    combined_artist["instagram_sns_score"] = 0
            else:
                combined_artist["instagram_sns_score"] = 0
            combined_artist_sns_score.append(combined_artist)

        return combined_artist_sns_score

    @staticmethod
    def calculate_sns_score(merge_list):
        # Calculate total_sns_score for each artist
        for item in merge_list:
            # Calculate sns score
            youtube_sns_score = item.get('youtube_sns_score', 0)
            tiktok_sns_score = item.get('tiktok_sns_score', 0)
            instagram_sns_score = item.get('instagram_sns_score', 0)
            item['total_sns_score'] = youtube_sns_score + tiktok_sns_score + instagram_sns_score

        # Sort by total_score in descending order
        sorted_list = sorted(merge_list, key=lambda x: x['total_sns_score'], reverse=True)

        return sorted_list

    @classmethod
    def get_sns_score(self):
        try:
            combined_list = self.get_artist_sns_score()
            total_sns_score = self.calculate_sns_score(combined_list)

            return total_sns_score
        except Exception as e:
            return jsonify({
                'status': 'error',
                'err': str(e)
            }), 500

    @classmethod
    def calculate_overall_popularity(cls, country, year, week, type):
        # Validate required parameters
        if not country:
            return jsonify({'err': 'Missing country parameter'}), 400
        if not year:
            return jsonify({'err': 'Missing year parameter'}), 400
        if not week:
            return jsonify({'err': 'Missing week parameter'}), 400

        try:
            # request sns/ music/ drama endpoint separately
            music = cls.get_music_score(country, year, week)
            sns = cls.get_sns_score()
            drama = cls.get_drama_score(country, year, week)

            # Merge the data
            result = cls.merge_all(sns, music, drama)

            # filter data by type: actor/ musician
            actor_rank = [a for a in result if a.get("type") and "Actor" in a["type"]]
            musician_rank = [a for a in result if a.get("type") and "Musician" in a["type"]]

            # sort by popularity score
            actor_ranked = sorted(actor_rank, key=lambda x: x["popularity_score"], reverse=True)
            actor_top_result = actor_ranked[:100]
            for i, a in enumerate(actor_top_result, start=1):
                a["rank"] = i

            musician_ranked = sorted(musician_rank, key=lambda x: x["popularity_score"], reverse=True)
            musician_top_result = musician_ranked[:100]
            for i, m in enumerate(musician_top_result, start=1):
                m["rank"] = i

            overall_ranked = sorted(result, key=lambda x: x["popularity_score"], reverse=True)
            overall_top_result = overall_ranked[:100]
            # Add rank field based on total popularity score
            for index, artist in enumerate(overall_top_result, start=1):
                artist["rank"] = index

            if type:
                if type.lower() == "actor":
                    return jsonify({'status': 'success', 'data': actor_top_result}), 200
                elif type.lower() == "musician":
                    return jsonify({'status': 'success', 'data': musician_top_result}), 200

            return jsonify({
                'status': 'success',
                'data': overall_top_result
            }), 200

        except Exception as e:
            return jsonify({
                'status': 'error',
                'err': str(e)
            }), 500

    @staticmethod
    def merge_all(sns_list, music_list, drama_list):
        # Create dictionaries for faster lookup
        sns_dict = {item['artist']: item for item in sns_list}
        music_dict = {item['artist']: item for item in music_list}

        merged = []
        # Process artists in both lists
        common_artists = set(sns_dict.keys()) & set(music_dict.keys())
        for artist in common_artists:
            merged_item = {**sns_dict[artist], **music_dict[artist]}
            merged_item['sub_score'] = merged_item['total_sns_score'] + merged_item['total_music_score']
            merged.append(merged_item)

        # Process artists only in sns list
        sns_only = set(sns_dict.keys()) - set(music_dict.keys())
        for artist in sns_only:
            merged_item = sns_dict[artist].copy()
            merged_item['total_music_score'] = 0
            merged_item['sub_score'] = merged_item['total_sns_score']
            merged.append(merged_item)

        # Process artists only in music list
        music_only = set(music_dict.keys()) - set(sns_dict.keys())
        for artist in music_only:
            merged_item = music_dict[artist].copy()
            merged_item['total_sns_score'] = 0
            merged_item['sub_score'] = merged_item['total_music_score']
            merged.append(merged_item)

        # merged = sorted(merged, key=lambda x: x['sub_score'], reverse=True)
        # Merge with drama list
        # Create a dictionary for drama artists with artist_id as key
        drama_dict = {item['artist_id']: item for item in drama_list}

        second_merge = []
        # Process all sub_results items
        for item in merged:
            sec_merged_item = item.copy()

            # Check if this artist exists in drama list
            if 'artist_id' in item and item['artist_id'] in drama_dict:
                drama_data = drama_dict[item['artist_id']]
                sec_merged_item['total_drama_score'] = drama_data['total_drama_score']
                sec_merged_item['popularity_score'] = item['sub_score'] + drama_data['total_drama_score']

                # Add drama-specific fields if they exist
                if 'english_name' in drama_data:
                    sec_merged_item['english_name'] = drama_data['english_name']
                if 'name' in drama_data:
                    sec_merged_item['name'] = drama_data['name']
            else:
                sec_merged_item['total_drama_score'] = 0
                sec_merged_item['popularity_score'] = item['sub_score']

            second_merge.append(sec_merged_item)

        # Add drama artists not in sub_results
        sub_result_ids = {item['artist_id'] for item in merged if 'artist_id' in item}
        for drama_item in drama_list:
            if drama_item['artist_id'] not in sub_result_ids:
                sec_merged_item = {
                    'artist_id': drama_item['artist_id'],
                    'total_drama_score': drama_item['total_drama_score'],
                    'popularity_score': drama_item['total_drama_score'],
                    'sub_score': 0,
                    'type': drama_item['type']
                }

                # Add available fields
                if 'english_name' in drama_item:
                    sec_merged_item['english_name'] = drama_item['english_name']
                if 'name' in drama_item:
                    sec_merged_item['name'] = drama_item['name']
                if 'instagram_id' in drama_item:
                    sec_merged_item['instagram_id'] = drama_item['instagram_id']
                if 'tiktok_id' in drama_item:
                    sec_merged_item['tiktok_id'] = drama_item['tiktok_id']
                if 'youtube_id' in drama_item:
                    sec_merged_item['youtube_id'] = drama_item['youtube_id']

                second_merge.append(sec_merged_item)

        # Return needed fields
        # Define the fields we want to keep for each artist
        fields_to_keep = {
            "artist", "artist_id", "country", "datetime", "day", "month", "year", "week",
            "popularity_score", "total_drama_score", "total_music_score", "total_sns_score",
            "spotify_id", "tiktok_id", "youtube_id", "instagram_id", "instagram_user",
            "korean_name", "type", "billboard_score", "youtube_score"
        }
        # Filter each dictionary to keep only the desired fields
        filtered_list = []
        for artist_data in second_merge:
            filtered_data = {key: value for key, value in artist_data.items() if key in fields_to_keep}
            filtered_list.append(filtered_data)

        # print(len(top_result))
        return filtered_list

    @classmethod
    def get_popularity_score(cls):
        pass
