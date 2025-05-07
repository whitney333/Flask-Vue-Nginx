from flask import request, jsonify
import json
import re
from models.artist_model import Artists
# music related data
from models.spotify_model import SpotifyCharts, SpotifyOst
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
        pipeline = [
            {"$match": {
                "artist_id": {"$ne": None}
            }},
            {"$project": {
                "_id": 0,
                "artist_id": "$artist_id",
                "english_name": "$english_name",
                "korean_name": "$korean_name",
                "instagram_id": "$instagram_id",
                "youtube_id": "$youtube_id",
                "tiktok_id": "$tiktok_id"
            }}
        ]

        artists = Artists.objects().aggregate(pipeline)
        results = []
        for artist in artists:
            results.append(artist)

        return results

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
                "mid": "$artist_info.artist_id",
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
    def merge_all_music_scores(cls, country, year, week):
        # music data
        sp_data = cls.get_spotify_charts_score(country, year, week)
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
        merge_music_data = self.merge_all_music_scores(country, year, week)

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
            spotify_score = item.get('sp_total_score', 0)
            item['total_music_score'] = youtube_score + billboard_score + spotify_score
            # Calculate sns score
            youtube_sns_score = item.get('youtube_sns_score', 0)
            tiktok_sns_score = item.get('tiktok_sns_score', 0)
            instagram_sns_score = item.get('instagram_sns_score', 0)
            item['total_sns_score'] = youtube_sns_score + tiktok_sns_score + instagram_sns_score

        # Sort by total_score in descending order
        sorted_list = sorted(merge_list, key=lambda x: x['total_music_score'], reverse=True)

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
    def get_drama_score(cls, country, year, week):
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
    def get_sns_score(self):

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
                combined_artist["tiktok_sns_score"] = tk_sns_scores[0]["hashtag"]
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
            combined_list = self.get_sns_score()
            results = self.calculate_sns_score(combined_list)

            return jsonify({
                'status': 'success',
                'data': results
            }), 200
        except Exception as e:
            return jsonify({
                'err': str(e)
            }), 500
