from flask import request, jsonify
import json
import re
import pandas as pd
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
        Includes:
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
                "youtube_id": "$youtube_id",
                "tiktok_id": "$tiktok_id",
                "spotify_id": "$spotify_id"
            }}
        ]

        artists = Artists.objects().aggregate(pipeline)
        results = []
        for artist in artists:
            results.append(artist)

        return results

    @staticmethod
    def get_spotify_popularity(spotify_id):
        """
        To avoid artists do not enter any music charts,
        we add spotify popularity index as the base score
        :return:
        """
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
        result = []

        for item in results:
            result.append(item)

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

    @classmethod
    def merge_spotify_score(cls, country, year, week):
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
                    "type": chart_item["type"],
                    "country": chart_item["country"],
                    "year": chart_item["year"],
                    "month": chart_item["month"],
                    "day": chart_item["day"],
                    "week": chart_item["week"],
                    "datetime": chart_item["datetime"],
                    "instagram_id": pop_match["instagram_id"],
                    "instagram_user": chart_item["instagram_user"],
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

        return final_result

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
                "from": "artists",
                "localField": "sp_id",
                "foreignField": "spotify_id",
                "as": "artist_info"
            }},
            # unwind artist_info field and simultaneously keep other records which do not have this field
            {"$unwind": {
                "path": "$artist_info",
                "preserveNullAndEmptyArrays": True
            }},
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
                "type": "$artist_info.type",
                "mid": "$artist_info.artist_id",
                "sp_chart_score": "$sp_total_score",
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

        return sorted_list

    @classmethod
    def get_music_score(cls, country, year, week):
        if not all([country, year, week]):
            return jsonify({'err': 'Missing required parameters'}), 400

        try:
            merge_list = cls.merge_music_scores(country, year, week)
            results = cls.calculate_total_music_score(merge_list)

            return jsonify({
                'status': 'success',
                'data': results
            }), 200
        except Exception as e:
            return jsonify({
                'err': str(e)
            }), 500

    @staticmethod
    def get_netflix_chart(country, year, week):
        if not all([country, year, week]):
            return jsonify({'err': 'Missing required parameters'}), 400

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
                "week": week
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
                "rank_score": {"$toInt": "$rank_score"},
                "name": "$name",
                "weeks_on_chart": "$weeks_on_chart"
            }}
        ]

        try:
            results = NetflixCharts.objects().aggregate(pipeline)
            result = []
            for item in results:
                result.append(item)
            # print(result)
            return result
        except Exception as e:
            return jsonify({'err': str(e)}), 500

    @staticmethod
    def get_spotify_ost(year, week):
        if not all([year, week]):
            return jsonify({'err': 'Missing required parameters'}), 400

        year = int(year)
        pipeline = [
            {"$match": {
                "BROADCAST_YEAR": {
                    "$gte": year-1,
                    "$lte": year
                }
            }},
            {"$project": {
                "english_name": "$NAME",
                "korean_name": "$NAME_IN_KOREAN",
                "artist_id": "$STARRING.MID"
            }},
            # lookup spotify ost
            {"$lookup": {
                "from": "spotify_ost",
                "let": {"english_name": "$english_name"},
                "pipeline": [
                    {"$match": {
                        "year": year,
                        "week": week
                    }}
                ],
                "as": "spotify_ost"
            }},
            {"$unwind": "$spotify_ost"},
            # match drama name with album name
            {"$addFields": {
                "is_match": {
                    "$regexMatch": {
                        "input": "$spotify_ost.album",
                        "regex": {
                            "$concat": [".*", {"$toString": "$english_name"}, ".*"]
                        },
                        "options": "i"
                    }
                }
            }},
            # return matched drama
            {"$match": {
                "is_match": True
            }},
            # group by drama
            {"$group": {
                "_id": "$english_name",
                "korean_name": {"$first": "$korean_name"},
                "artist_id": {"$first": "$artist_id"},
                "year": {"$first": "$spotify_ost.year"},
                "week": {"$first": "$spotify_ost.week"},
                "play_counts": {"$push": {"$toInt": "$spotify_ost.play_counts"}}
            }},
            # return sum up play_counts
            {"$project": {
                "_id": 0,
                "english_name": "$_id",
                "korean_name": "$korean_name",
                "artist_id": "$artist_id",
                "year": "$year",
                "week": "$week",
                "play_counts": {"$sum": "$play_counts"}
            }},
            {"$unwind": "$artist_id"},
            {"$group": {
                "_id": "$artist_id",
                "english_name": {"$push": "$english_name"},
                "korean_name": {"$push": "$korean_name"},
                "year": {"$first": "$year"},
                "week": {"$first": "$week"},
                "ost_score": {"$push": "$play_counts"}
            }}
        ]

        try:
            results = Drama.objects().aggregate(pipeline)
            result = []
            for item in results:
                result.append(item)
            # print(result)
            return result
        except Exception as e:
            return jsonify({
                'err': str(e)
            }), 500

    @staticmethod
    def get_all_drama(year):
        if not all([year]):
            return jsonify({'err': 'Missing required parameters'}), 400

        year = int(year)
        pipeline = [
            {"$match": {
                "BROADCAST_YEAR": {
                    "$gte": year - 1,  # fetch drama within 2 yrs
                    "$lt": year
                }
            }},
            {"$project": {
                "_id": 0,
                "english_name": "$NAME",
                "korean_name": "$NAME_IN_KOREAN",
                "artist_id": "$STARRING.MID"
            }},
        ]

        try:
            results = Drama.objects().aggregate(pipeline)
            result = []
            for item in results:
                result.append(item)
            # print(result)
            return result
        except Exception as e:
            return jsonify({
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

    @classmethod
    def merge_drama_score(cls, country, year, week):
        if not all([country, year, week]):
            return jsonify({'err': 'Missing required parameters'}), 400

        # get spotify ost list
        ost = cls.get_spotify_ost(year, week)
        ost_dict = {}

        for item in ost:
            # Handle both single names and lists of names
            english_names = item['english_name'] if isinstance(item['english_name'], list) else [item['english_name']]
            for name in english_names:
                base_name = cls.extract_base_title(name)
                if base_name not in ost_dict:
                    ost_dict[base_name] = []
                ost_dict[base_name].append(item)

        # match global netflix chart as default
        netflix = cls.get_netflix_chart(country, year, week)

        result = []

        for netflix_item in netflix:
            netflix_base = cls.extract_base_title(netflix_item['name'])
            matched_ost_items = ost_dict.get(netflix_base, [])

            if matched_ost_items:
                for ost_item in matched_ost_items:
                    # Merge the dictionaries (netflix fields first, then ost fields)
                    merged = {"name": netflix_item.get("name"),
                              "country": netflix_item.get("country"),
                              "netflix_score": netflix_item.get("rank_score"),
                              "year": netflix_item.get("year"),
                              "week": netflix_item.get("week"),
                              "artist_id": ost_item.get("_id"),
                              "korean_name": ost_item.get("korean_name")[0],
                              "ost_score": ost_item.get("ost_score")[0]
                              }
                    result.append(merged)

        return result

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
                "artist": "$english_name",
                "korean_name": "$korean_name",
                "instagram_id": "$instagram_id",
                "youtube_id": "$youtube_id",
                "tiktok_id": "$tiktok_id",
                "spotify_id": "$spotify_id"
            }}
        ]

        artists = Artists.objects().aggregate(pipeline)
        results = []
        for artist in artists:
            results.append(artist)

        return results

    @classmethod
    def merge_drama_with_ids(cls, country, year, week):
        merged_drama = cls.get_drama_score(country, year, week)

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
            return jsonify({
                'status': 'success',
                'data': combined_list
            })
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
    def get_drama_score(cls, country, year, week):
        if not all([country, year, week]):
            return jsonify({'err': 'Missing required parameters'}), 400

        merge_list = cls.merge_drama_score(country, year, week)
        results = cls.calculate_total_drama_score(merge_list)

        return results

    @staticmethod
    def get_instagram_score(artist_id):
        """
        Get Instagram latest 12 posts' total likes & comments,
        and 7-day follower growth
        :return:
        """
        if not all([artist_id]):
            return jsonify({'err': 'Missing required parameters'}), 400

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
                }},
                {"$lookup": {
                    "from": "instagram",
                    "let": {"user_id": "$user_id", "datetime": "$datetime"},
                    "pipeline": [
                        {"$match": {
                            "$expr": {"$eq": ["$user_id", "$$user_id"]}
                        }},
                        {"$sort": {"datetime": -1}},
                        {"$limit": 7}
                    ],
                    'as': 'matched_ins'
                }},
                {"$unwind": "$matched_ins"},
                {"$group": {
                    "_id": "$user_id",
                    "datetime": {"$first": "$datetime"},
                    "engagement_score": {"$first": "$engagement_score"},
                    "follower": {"$push": "$matched_ins.follower_count"}
                }},
                # return fields
                {"$project": {
                    "_id": 0,
                    # "datetime": "$datetime",
                    # "user_id": "$_id",
                    "instagram_score": {
                        "$sum": [{
                            "$subtract": [
                                {"$arrayElemAt": ["$follower", 0]}, {"$arrayElemAt": ["$follower", -1]}
                            ]
                        }, "$engagement_score"]
                    },
                }}
            ]

            results = InstagramLatest.objects().aggregate(pipeline)
            result = []
            for item in results:
                result.append(item)

            return result
        except Exception as e:
            return jsonify({
                'err': str(e)
            }), 500

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
                    "channel_id": "$channel_id",
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
    def get_db_sns_score(self):
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
    def get_total_sns_score(self):
        try:
            combined_list = self.get_db_sns_score()
            results = self.calculate_sns_score(combined_list)

            return jsonify({
                'status': 'success',
                'data': results
            }), 200
        except Exception as e:
            return jsonify({
                'err': str(e)
            }), 500

    @classmethod
    def calculate_overall_popularity(cls, country, year, week):
        # request sns/ music/ drama endpoint separately
        music = cls.get_music_score(country, year, week)
        sns = cls.get_total_sns_score()
        drama = cls.get_drama_score(country, year, week)

        # Convert lists to DataFrames
        df_music = pd.DataFrame(music)
        df_sns = pd.DataFrame(sns)
        df_drama = pd.DataFrame(drama)

        results = []
        # get all unique artist_ids from all datasets
        all_artist_ids = set(df_music['artist_id'].dropna().unique()).union(
            set(df_sns['artist_id'].dropna().unique())).union(
            set(df_drama['artist_id'].dropna().unique()))

        for artist_id in all_artist_ids:
            result = {
                "artist_id": artist_id,
                "country": country,
                "week": week,
                "year": year,
                "total_drama_score": None,
                "total_sns_score": None,
                "total_music_score": None,
                "youtube_id": None,
                "tiktok_id": None,
                "spotify_id": None,
                "popularity": None
            }

            # initialize scores for popularity calculation
            drama_score = 0
            sns_score = 0
            music_score = 0

            # get music data if exists
            music_data = df_music[df_music['artist_id'] == artist_id]
            if not music_data.empty:
                music_data = music_data.iloc[0].to_dict()
                music_score = music_data.get("total_music_score", 0)
                result.update({
                    "country": music_data.get("country", "south-korea"),
                    "total_music_score": music_score,
                    "spotify_id": music_data.get("spotify_id"),
                    "youtube_id": music_data.get("youtube_id"),
                    "tiktok_id": music_data.get("tiktok_id")
                })

            # get sns data if exists
            sns_data = df_sns[df_sns['artist_id'] == artist_id]
            if not sns_data.empty:
                sns_data = sns_data.iloc[0].to_dict()
                sns_score = sns_data.get("total_sns_score", 0)
                result.update({
                    "total_sns_score": sns_score,
                    "youtube_id": sns_data.get("youtube_id") or result["youtube_id"],
                    "tiktok_id": sns_data.get("tiktok_id") or result["tiktok_id"],
                    "spotify_id": sns_data.get("spotify_id") or result["spotify_id"],
                    "country": sns_data.get("country", result["country"])
                })

            # get drama data if exists
            drama_data = df_drama[df_drama['artist_id'] == artist_id]
            if not drama_data.empty:
                drama_data = drama_data.iloc[0].to_dict()
                drama_score = drama_data.get("total_drama_score", 0)
                result.update({
                    "total_drama_score": drama_score,
                    "country": drama_data.get("country", result["country"])
                })

            # Calculate popularity (handle None values by treating them as 0)
            result["popularity"] = (drama_score if drama_score is not None else 0) + \
                                   (sns_score if sns_score is not None else 0) + \
                                   (music_score if music_score is not None else 0)

            results.append(result)

        return results

    ########################################################
    # V1 API methods for Trending Artists feature
    ########################################################

    @classmethod
    def get_trending_rank(cls, country, year, week):
        """
        Get ranked list of artists by popularity for a given country/region.
        Wraps calculate_overall_popularity and adds artist details from DB.

        :param country: Country/region code (e.g., 'global', 'south-korea', 'taiwan')
        :param year: Year for the data
        :param week: Week number for the data
        :return: JSON response with ranked artist list
        """
        if not all([country, year, week]):
            return jsonify({'error': 'Missing required parameters: country, year, week'}), 400

        try:
            # Get popularity data
            popularity_data = cls.calculate_overall_popularity(country, year, week)

            # Sort by popularity descending
            sorted_data = sorted(popularity_data, key=lambda x: x.get('popularity', 0) or 0, reverse=True)

            # Enrich with artist details from database
            results = []
            for rank, item in enumerate(sorted_data, start=1):
                artist_id = item.get('artist_id')

                # Query artist details from database
                artist_info = cls.get_db_artist_ids(artist_id)

                artist_data = {
                    'rank': rank,
                    'artist_id': artist_id,
                    'english_name': None,
                    'korean_name': None,
                    'image_url': None,
                    'type': None,
                    'nation': None,
                    'popularity': item.get('popularity', 0),
                    'total_music_score': item.get('total_music_score', 0),
                    'total_sns_score': item.get('total_sns_score', 0),
                    'total_drama_score': item.get('total_drama_score', 0),
                    'instagram_id': None,
                    'instagram_user': None,
                    'youtube_id': item.get('youtube_id'),
                    'tiktok_id': item.get('tiktok_id'),
                    'spotify_id': item.get('spotify_id'),
                }

                # If artist found in database, enrich with details
                if artist_info and len(artist_info) > 0:
                    db_artist = artist_info[0]
                    artist_data.update({
                        'english_name': db_artist.get('artist'),
                        'korean_name': db_artist.get('korean_name'),
                        'type': db_artist.get('type'),
                        'instagram_id': db_artist.get('instagram_id'),
                        'youtube_id': db_artist.get('youtube_id') or artist_data['youtube_id'],
                        'tiktok_id': db_artist.get('tiktok_id') or artist_data['tiktok_id'],
                        'spotify_id': db_artist.get('spotify_id') or artist_data['spotify_id'],
                    })

                # Get additional artist info (image_url, nation) from Artist model
                try:
                    artist_doc = Artists.objects(artist_id=artist_id).first()
                    if artist_doc:
                        artist_data['image_url'] = artist_doc.image_url
                        artist_data['nation'] = artist_doc.nation
                        artist_data['instagram_user'] = artist_doc.instagram_user
                except Exception:
                    pass

                results.append(artist_data)

            return jsonify({
                'status': 'success',
                'country': country,
                'year': year,
                'week': week,
                'total_count': len(results),
                'data': results
            }), 200

        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @classmethod
    def get_artist_scores(cls, artist_id, year, week):
        """
        Get popularity, SNS, music, and drama scores for an artist.
        For artist details, use /api/artist/v1/artist/<artist_id> instead.

        :param artist_id: The artist's unique identifier
        :param year: Year for the score data
        :param week: Week number for the score data
        :return: JSON response with artist scores
        """
        if not all([artist_id, year, week]):
            return jsonify({'error': 'Missing required parameters: artist_id, year, week'}), 400

        try:
            result = {
                'artist_id': artist_id,
                'year': year,
                'week': week,
                'popularity': 0,
                'total_music_score': 0,
                'total_sns_score': 0,
                'total_drama_score': 0,
                'global_rank': None,
            }

            # Calculate scores using existing calculate_overall_popularity
            popularity_data = cls.calculate_overall_popularity('global', year, week)

            # Find this artist in the data
            artist_scores = next(
                (item for item in popularity_data if item.get('artist_id') == artist_id),
                None
            )

            if artist_scores:
                result['popularity'] = artist_scores.get('popularity', 0)
                result['total_music_score'] = artist_scores.get('total_music_score', 0)
                result['total_sns_score'] = artist_scores.get('total_sns_score', 0)
                result['total_drama_score'] = artist_scores.get('total_drama_score', 0)

            # Calculate global rank
            sorted_data = sorted(popularity_data, key=lambda x: x.get('popularity', 0) or 0, reverse=True)
            for rank, item in enumerate(sorted_data, start=1):
                if item.get('artist_id') == artist_id:
                    result['global_rank'] = rank
                    break

            return jsonify({
                'status': 'success',
                'data': result
            }), 200

        except Exception as e:
            return jsonify({'error': str(e)}), 500
