from models.sns.youtube_model import YoutubeVideo, Youtube
import pandas as pd
import numpy as np
import datetime
from flask import jsonify, request


class YoutubeController:
    @staticmethod
    def extract_hashtags_keyword(text):
        """
        extract keywords with hashtag from string
        """
        # initializing hashtag_list variable
        hashtag_list = []

        # splitting the text into words
        for word in text.split():
            # checking the first character of every word
            if word[0] == '#':
                # adding the word to the hashtag_list
                hashtag_list.append(word[1:])
        return hashtag_list

    @classmethod
    #add this, if you need to call other functions in the same class
    def get_hashtags_most_used_recent_five(self, artist_id):
        # Validate required parameters
        if not artist_id:
            return jsonify({'err': 'Missing artist_id parameter'}), 400

        try:
            pipeline = [
            # match artist channel id
            {"$match": {
                "channel_id": artist_id
            }},
            {"$sort": {"datetime": -1}},
            {"$limit": 1},
            {"$unwind": "$video"},
            # get latest 5 posts
            {"$limit": 5},
            {"$project": {
                "_id": 0,
                "published_date": "$video.published_at",
                "title": "$video.title",
                "tags": "$video.tags"
            }},
            {"$set": {
                "n": {
                    "$replaceOne": {
                        "input": "$title",
                        "find": "#",
                        "replacement": " #"
                    }
                }
            }}
        ]

            results = Youtube.objects.aggregate(pipeline)


            _temp_list = []
            for item in results:
                _temp_list.append(item)

            # flatten item in list
            _tag = [ele.get("tags") for ele in _temp_list]
            _title = [self.extract_hashtags_keyword(ele["n"]) for ele in _temp_list]
            # print(_title)
            # print(_tag)
            flat_title = [item for sublist in _title for item in sublist]
            # print(flat_title)

            # replace None value to ''
            _switch_none = ['' if v is None else v for v in _tag]
            # flatten tags list
            flat_tag = [item for sublist in _switch_none for item in sublist]
            # print(flat_tag)

            # concatenate two lists, and count occurrence value
            joined_list = flat_title + flat_tag
            w = pd.value_counts(np.array(joined_list))

            # convert list to df then dict
            df = pd.DataFrame(list(zip(w.keys(), w)), columns=['_id', 'count'])
            result = df.to_dict(orient='records')[:10]


            return jsonify({
                'status': 'success',
                'data': result
            }), 200
        except Exception as e:
            return jsonify({
                'status': 'error',
                'err': str(e)
            })

    @classmethod
    def get_hashtags_most_used_recent_eight(self, artist_id):
        # Validate required parameters
        if not artist_id:
            return jsonify({'err': 'Missing artist_id parameter'}), 400

        try:
            pipeline = [
            # match artist channel id
            {"$match": {
                "channel_id": artist_id
            }},
            {"$sort": {"datetime": -1}},
            {"$limit": 1},
            {"$unwind": "$video"},
            # get latest 8 posts
            {"$limit": 8},
            {"$project": {
                "_id": 0,
                "published_date": "$video.published_at",
                "title": "$video.title",
                "tags": "$video.tags"
            }},
            {"$set": {
                "n": {
                    "$replaceOne": {
                        "input": "$title",
                        "find": "#",
                        "replacement": " #"
                    }
                }
            }}
        ]

            results = Youtube.objects.aggregate(pipeline)


            _temp_list = []
            for item in results:
                _temp_list.append(item)

            # flatten item in list
            _tag = [ele.get("tags") for ele in _temp_list]
            _title = [self.extract_hashtags_keyword(ele["n"]) for ele in _temp_list]
            # print(_title)
            # print(_tag)
            flat_title = [item for sublist in _title for item in sublist]
            # print(flat_title)

            # replace None value to ''
            _switch_none = ['' if v is None else v for v in _tag]
            # flatten tags list
            flat_tag = [item for sublist in _switch_none for item in sublist]
            # print(flat_tag)

            # concatenate two lists, and count occurrence value
            joined_list = flat_title + flat_tag
            w = pd.value_counts(np.array(joined_list))

            # convert list to df then dict
            df = pd.DataFrame(list(zip(w.keys(), w)), columns=['_id', 'count'])
            result = df.to_dict(orient='records')[:10]

            return jsonify({
                'status': 'success',
                'data': result
            }), 200
        except Exception as e:
            return jsonify({
                'status': 'error',
                'err': str(e)
            })

    @classmethod
    def get_hashtags_most_used_recent_twelve(self, artist_id):
        # Validate required parameters
        if not artist_id:
            return jsonify({'err': 'Missing artist_id parameter'}), 400

        try:
            pipeline = [
            # match artist channel id
            {"$match": {
                "channel_id": artist_id
            }},
            {"$sort": {"datetime": -1}},
            {"$limit": 1},
            {"$unwind": "$video"},
            # get latest 12 posts
            {"$limit": 12},
            {"$project": {
                "_id": 0,
                "published_date": "$video.published_at",
                "title": "$video.title",
                "tags": "$video.tags"
            }},
            {"$set": {
                "n": {
                    "$replaceOne": {
                        "input": "$title",
                        "find": "#",
                        "replacement": " #"
                    }
                }
            }}
        ]

            results = Youtube.objects.aggregate(pipeline)


            _temp_list = list(results)

            # flatten item in list
            _tag = [ele.get("tags") for ele in _temp_list]
            _title = [self.extract_hashtags_keyword(ele["n"]) for ele in _temp_list]
            # print(_title)
            # print(_tag)
            flat_title = [item for sublist in _title for item in sublist]
            # print(flat_title)

            # replace None value to ''
            _switch_none = ['' if v is None else v for v in _tag]
            # flatten tags list
            flat_tag = [item for sublist in _switch_none for item in sublist]
            # print(flat_tag)

            # concatenate two lists, and count occurrence value
            joined_list = flat_title + flat_tag
            w = pd.value_counts(np.array(joined_list))

            # convert list to df then dict
            df = pd.DataFrame(list(zip(w.keys(), w)), columns=['_id', 'count'])
            result = df.to_dict(orient='records')[:10]

            # print(result)

            return jsonify({
                'status': 'success',
                'data': result
            }), 200
        except Exception as e:
            return jsonify({
                'status': 'error',
                'err': str(e)
            })

    @classmethod
    def get_hashtags_most_engaged_recent_five(self, artist_id):
        # Validate required parameters
        if not artist_id:
            return jsonify({'err': 'Missing artist_id parameter'}), 400

        try:
            pipeline = [
                {"$match": {
                        "channel_id": artist_id
                }},
                {"$sort": {"datetime": -1}},
                {"$limit": 1},
                {"$unwind": "$video"},
                {"$project": {
                    "_id": 0,
                    "datetime": "$datetime",
                    "publish_at": "$video.published_at",
                    "title": "$video.title",
                    "sub_total": {"$sum": ["$video.like_count", "$video.comment_count"]},
                    "view_count": "$video.view_count",
                    "hashtags": "$video.tags",
                    "follower": "$subscriber_count"
                }},
                # replace # in title
                {"$set": {
                    "n": {
                        "$replaceOne": {
                            "input": "$title",
                            "find": "#",
                            "replacement": " #"
                        }
                    }
                }},
                {"$project": {
                    "datetime": "$datetime",
                    "publish_at": "$publish_at",
                    "title": "$title",
                    "sub_total": "$sub_total",
                    "tags": "$hashtags",
                    "follower": "$follower",
                    "view_count": "$view_count",
                    "nn": {
                        "$split": ["$n", " "]
                    }
                }},
                {"$sort": {"publish_at": -1}},
                # limit posts
                {"$limit": 5},
                {"$unwind": "$nn"},
                {"$addFields": {
                    "_cleaned": {
                        "$regexFindAll": {
                            "input": "$nn",
                            "regex": "#.*"
                        }
                    }
                }},
                {"$project": {
                    "datetime": "$datetime",
                    "publish_at": "$publish_at",
                    "title": "$title",
                    "sub_total": "$sub_total",
                    "tags": "$tags",
                    "follower": "$follower",
                    "view_count": {"$toInt": "$view_count"},
                    "_new": {
                        "$concatArrays": [
                            {"$ifNull": ["$_cleaned.match", []]},
                            {"$ifNull": ["$tags", []]}
                        ]
                    }
                }},
                {"$unwind": "$_new"},
                {"$addFields": {
                    "_eng_rate": {"$divide": ["$sub_total", "$view_count"]}
                }},
                # groupby hashtag
                {"$group": {
                    "_id": "$_new",
                    "count": {"$sum": 1},
                    "_total_eng_rate": {"$sum": "$_eng_rate"}
                }},
                {"$project": {
                    "eng_rate_per_hashtag": {
                        "$divide": ["$_total_eng_rate", "$count"]
                    }
                }},
                {"$project": {
                    "eng_rate_per_hashtag": {
                        "$multiply": ["$eng_rate_per_hashtag", 100]
                    }
                }},
                {"$sort": {"eng_rate_per_hashtag": -1}},
                {"$limit": 10}
            ]

            results = Youtube.objects.aggregate(pipeline)

            result = list(results)

            return jsonify({
                'status': 'success',
                'data': result
            })
        except Exception as e:
            return jsonify({
                'status': 'error',
                'err': str(e)
            })

    @classmethod
    def get_hashtags_most_engaged_recent_eight(self, artist_id):
        # Validate required parameters
        if not artist_id:
            return jsonify({'err': 'Missing artist_id parameter'}), 400

        try:
            pipeline = [
                {"$match": {
                        "channel_id": artist_id
                }},
                {"$sort": {"datetime": -1}},
                {"$limit": 1},
                {"$unwind": "$video"},
                {"$project": {
                    "_id": 0,
                    "datetime": "$datetime",
                    "publish_at": "$video.published_at",
                    "title": "$video.title",
                    "sub_total": {"$sum": ["$video.like_count", "$video.comment_count"]},
                    "view_count": "$video.view_count",
                    "hashtags": "$video.tags",
                    "follower": "$subscriber_count"
                }},
                # replace # in title
                {"$set": {
                    "n": {
                        "$replaceOne": {
                            "input": "$title",
                            "find": "#",
                            "replacement": " #"
                        }
                    }
                }},
                {"$project": {
                    "datetime": "$datetime",
                    "publish_at": "$publish_at",
                    "title": "$title",
                    "sub_total": "$sub_total",
                    "tags": "$hashtags",
                    "follower": "$follower",
                    "view_count": "$view_count",
                    "nn": {
                        "$split": ["$n", " "]
                    }
                }},
                {"$sort": {"publish_at": -1}},
                # limit posts
                {"$limit": 8},
                {"$unwind": "$nn"},
                {"$addFields": {
                    "_cleaned": {
                        "$regexFindAll": {
                            "input": "$nn",
                            "regex": "#.*"
                        }
                    }
                }},
                {"$project": {
                    "datetime": "$datetime",
                    "publish_at": "$publish_at",
                    "title": "$title",
                    "sub_total": "$sub_total",
                    "tags": "$tags",
                    "follower": "$follower",
                    "view_count": {"$toInt": "$view_count"},
                    "_new": {
                        "$concatArrays": [
                            {"$ifNull": ["$_cleaned.match", []]},
                            {"$ifNull": ["$tags", []]}
                        ]
                    }
                }},
                {"$unwind": "$_new"},
                {"$addFields": {
                    "_eng_rate": {"$divide": ["$sub_total", "$view_count"]}
                }},
                # groupby hashtag
                {"$group": {
                    "_id": "$_new",
                    "count": {"$sum": 1},
                    "_total_eng_rate": {"$sum": "$_eng_rate"}
                }},
                {"$project": {
                    "eng_rate_per_hashtag": {
                        "$divide": ["$_total_eng_rate", "$count"]
                    }
                }},
                {"$project": {
                    "eng_rate_per_hashtag": {
                        "$multiply": ["$eng_rate_per_hashtag", 100]
                    }
                }},
                {"$sort": {"eng_rate_per_hashtag": -1}},
                {"$limit": 10}
            ]

            results = Youtube.objects.aggregate(pipeline)

            result = list(results)

            return jsonify({
                'status': 'success',
                'data': result
            })
        except Exception as e:
            return jsonify({
                'status': 'error',
                'err': str(e)
            })

    @classmethod
    def get_hashtags_most_engaged_recent_twelve(self, artist_id):
        # Validate required parameters
        if not artist_id:
            return jsonify({'err': 'Missing artist_id parameter'}), 400

        try:
            pipeline = [
                {"$match": {
                        "channel_id": artist_id
                }},
                {"$sort": {"datetime": -1}},
                {"$limit": 1},
                {"$unwind": "$video"},
                {"$project": {
                    "_id": 0,
                    "datetime": "$datetime",
                    "publish_at": "$video.published_at",
                    "title": "$video.title",
                    "sub_total": {"$sum": ["$video.like_count", "$video.comment_count"]},
                    "view_count": "$video.view_count",
                    "hashtags": "$video.tags",
                    "follower": "$subscriber_count"
                }},
                # replace # in title
                {"$set": {
                    "n": {
                        "$replaceOne": {
                            "input": "$title",
                            "find": "#",
                            "replacement": " #"
                        }
                    }
                }},
                {"$project": {
                    "datetime": "$datetime",
                    "publish_at": "$publish_at",
                    "title": "$title",
                    "sub_total": "$sub_total",
                    "tags": "$hashtags",
                    "follower": "$follower",
                    "view_count": "$view_count",
                    "nn": {
                        "$split": ["$n", " "]
                    }
                }},
                {"$sort": {"publish_at": -1}},
                # limit posts
                {"$limit": 12},
                {"$unwind": "$nn"},
                {"$addFields": {
                    "_cleaned": {
                        "$regexFindAll": {
                            "input": "$nn",
                            "regex": "#.*"
                        }
                    }
                }},
                {"$project": {
                    "datetime": "$datetime",
                    "publish_at": "$publish_at",
                    "title": "$title",
                    "sub_total": "$sub_total",
                    "tags": "$tags",
                    "follower": "$follower",
                    "view_count": {"$toInt": "$view_count"},
                    "_new": {
                        "$concatArrays": [
                            {"$ifNull": ["$_cleaned.match", []]},
                            {"$ifNull": ["$tags", []]}
                        ]
                    }
                }},
                {"$unwind": "$_new"},
                {"$addFields": {
                    "_eng_rate": {"$divide": ["$sub_total", "$view_count"]}
                }},
                # groupby hashtag
                {"$group": {
                    "_id": "$_new",
                    "count": {"$sum": 1},
                    "_total_eng_rate": {"$sum": "$_eng_rate"}
                }},
                {"$project": {
                    "eng_rate_per_hashtag": {
                        "$divide": ["$_total_eng_rate", "$count"]
                    }
                }},
                {"$project": {
                    "eng_rate_per_hashtag": {
                        "$multiply": ["$eng_rate_per_hashtag", 100]
                    }
                }},
                {"$sort": {"eng_rate_per_hashtag": -1}},
                {"$limit": 10}
            ]

            results = Youtube.objects.aggregate(pipeline)

            result = list(results)

            return jsonify({
                'status': 'success',
                'data': result
            })
        except Exception as e:
            return jsonify({
                'status': 'error',
                'err': str(e)
            })

    @staticmethod
    def get_channel_basic(artist_id, date_end, range):
        """
        Get artist's subscribers count by different time range ()

        """
        # Validate required parameters
        if not artist_id:
            return jsonify({'err': 'Missing artist_id parameter'}), 400
        if not date_end:
            return jsonify({'err': 'Missing date_end parameter'}), 400
        if not range:
            return jsonify({'err': 'Missing range parameter'}), 400

        try:
            # Validate and parse date
            format = "%Y-%m-%d"
            try:
                date_end = datetime.datetime.strptime(date_end, format)
            except ValueError:
                return jsonify({'err': 'Invalid date format. Use YYYY-MM-DD'}), 400

            # Define range mapping
            range_days = {
                "7d": 7,
                "28d": 28,
                "90d": 90,
                "180d": 180,
                "365d": 365
            }

            # Get number of days from range mapping, default to 7 days if range not found
            days = range_days.get(range, 7)
            start_date = date_end - datetime.timedelta(days=days)

            # mongodb pipeline
            pipeline = [
                # match artist channel id
                {"$match": {
                    "channel_id": artist_id
                }},
                {"$sort": {"datetime": 1}},
                # match date range
                {"$match": {
                    "datetime": {
                        "$lte": date_end,
                        "$gt": start_date
                    }
                }},
                {"$project": {
                    "_id": 0,
                    "datetime": {
                        "$dateToString": {
                            "format": "%Y-%m-%d",
                            "date": "$datetime"
                        }
                    },
                    "channel_id": "$channel_id",
                    "follower": {"$toInt": "$subscriber_count"},
                    "video_count": {"$toInt": "$video_count"},
                    "view_count": {"$toInt": "$view_count"},
                    "channel_hashtag": {"$toInt": "$channel_hashtag"},
                    "video_hashtag": {"$toInt": "$video_hashtag"}
                }}
            ]

            # Execute pipeline
            results = Youtube.objects().aggregate(pipeline)

            # Format results
            result = list(results)  # Convert cursor to list

            # Check if we got any results
            if not result:
                return jsonify({
                    'status': 'success',
                    'data': [],
                    'message': 'No data found for the specified range'
                }), 200

            return jsonify({
                'status': 'success',
                'data': result
            }), 200
        except Exception as e:
            return jsonify({
                'status': 'error',
                'err': str(e)
            }), 500

    @staticmethod
    def get_youtube_channel_video(artist_id, date_end, range):
        # Validate required parameters
        if not artist_id:
            return jsonify({'err': 'Missing artist_id parameter'}), 400
        if not date_end:
            return jsonify({'err': 'Missing date_end parameter'}), 400
        if not range:
            return jsonify({'err': 'Missing range parameter'}), 400

        try:
            # Validate and parse date
            format = "%Y-%m-%d"
            try:
                date_end = datetime.datetime.strptime(date_end, format)
            except ValueError:
                return jsonify({'err': 'Invalid date format. Use YYYY-MM-DD'}), 400

            # Define range mapping
            range_days = {
                "7d": 7,
                "28d": 28,
                "90d": 90,
                "180d": 180,
                "365d": 365
            }

            # Get number of days from range mapping, default to 7 days if range not found
            days = range_days.get(range, 7)
            start_date = date_end - datetime.timedelta(days=days)

            pipeline = [
                # match artist channel id
                {"$match": {
                    "channel_id": artist_id
                }},
                {"$sort": {"datetime": 1}},
                # match date range
                {"$match": {
                    "datetime": {
                        "$lte": date_end,
                        "$gt": start_date
                    }
                }},
                {"$project": {
                    "_id": 0,
                    "datetime": {
                        "$dateToString": {
                            "format": "%Y-%m-%d",
                            "date": "$datetime"
                        }
                    },
                    "view_count": {"$toInt": "$view_count"},
                }}
            ]

        except Exception as e:
            return jsonify({
                'status': 'error',
                'err': str(e)
            })

    @staticmethod
    def get_youtube_channel_view(artist_id, date_end, range):
        # Validate required parameters
        if not artist_id:
            return jsonify({'err': 'Missing artist_id parameter'}), 400
        if not date_end:
            return jsonify({'err': 'Missing date_end parameter'}), 400
        if not range:
            return jsonify({'err': 'Missing range parameter'}), 400

        try:
            # Validate and parse date
            format = "%Y-%m-%d"
            try:
                date_end = datetime.datetime.strptime(date_end, format)
            except ValueError:
                return jsonify({'err': 'Invalid date format. Use YYYY-MM-DD'}), 400

            # Define range mapping
            range_days = {
                "7d": 7,
                "28d": 28,
                "90d": 90,
                "180d": 180,
                "365d": 365
            }

            # Get number of days from range mapping, default to 7 days if range not found
            days = range_days.get(range, 7)
            start_date = date_end - datetime.timedelta(days=days)

            # mongodb pipeline
            pipeline = [
                # match artist channel id
                {"$match": {
                    "channel_id": artist_id
                }},
                {"$sort": {"datetime": 1}},
                # match date range
                {"$match": {
                    "datetime": {
                        "$lte": date_end,
                        "$gt": start_date
                    }
                }},
                {"$project": {
                    "_id": 0,
                    "datetime": {
                        "$dateToString": {
                            "format": "%Y-%m-%d",
                            "date": "$datetime"
                        }
                    },
                    "view_count": {"$toInt": "$view_count"},
                }}
            ]

            # Execute pipeline
            results = Youtube.objects().aggregate(pipeline)

            # Format results
            result = list(results)  # Convert cursor to list

            # Check if we got any results
            if not result:
                return jsonify({
                    'status': 'success',
                    'data': [],
                    'message': 'No data found for the specified range'
                }), 200

            return jsonify({
                'status': 'success',
                'data': result
            }), 200
        except Exception as e:
            return jsonify({
                'status': 'error',
                'err': str(e)
            }), 500

    @staticmethod
    def get_youtube_video_view(artist_id, date_end, range):
        # Validate required parameters
        if not artist_id:
            return jsonify({'err': 'Missing artist_id parameter'}), 400
        if not date_end:
            return jsonify({'err': 'Missing date_end parameter'}), 400
        if not range:
            return jsonify({'err': 'Missing range parameter'}), 400

        try:
            # Validate and parse date
            format = "%Y-%m-%d"
            try:
                date_end = datetime.datetime.strptime(date_end, format)
            except ValueError:
                return jsonify({'err': 'Invalid date format. Use YYYY-MM-DD'}), 400

            # Define range mapping
            range_days = {
                "7d": 7,
                "28d": 28,
                "90d": 90,
                "180d": 180,
                "365d": 365
            }

            # Get number of days from range mapping, default to 7 days if range not found
            days = range_days.get(range, 7)
            start_date = date_end - datetime.timedelta(days=days)

            # mongodb pipeline
            pipeline = [
                {"$match": {
                        "channel_id": artist_id
                }},
                {"$sort": {"datetime": -1}},
                # match date range
                {"$match": {
                    "datetime": {
                        "$lte": date_end,
                        "$gt": start_date
                    }
                }},
                {"$unwind": "$video"},
                {"$project": {
                    "_id": 0,
                    "datetime": "$datetime",
                    "video_publish_at": "$video.published_at",
                    "video_view": "$video.view_count"
                }},
                {"$group": {
                    "_id": "$datetime",
                    "latest_ten": {"$push": "$$ROOT"}
                }},
                {"$project": {
                    "_id": 1,
                    "videos": {
                        "$slice": [{
                            "$map": {
                                "input": "$latest_ten",
                                "as": "video",
                                "in": {
                                    "datetime": "$$video.datetime",
                                    "video_publish_at": {
                                        "$dateFromString": {
                                            "dateString": "$$video.video_publish_at",
                                            "format": "%Y-%m-%dT%H:%M:%SZ"
                                        }
                                    },
                                    "video_view": {"$toInt": "$$video.video_view"}
                                }
                            }
                        }, 12]
                    }
                }},
                {"$addFields": {
                    "total_view": {
                        # Sum all video_view values in the array
                        "$sum": "$videos.video_view"
                    }
                }},
                {"$sort": {"_id": 1}},
                {"$project": {
                    "_id": 0,
                    "datetime": {"$dateToString": {
                        "format": "%Y-%m-%d",
                        "date": "$_id"
                    }},
                    "total_video_view": "$total_view"
                }}
            ]

            # Execute pipeline
            results = Youtube.objects().aggregate(pipeline)

            # Format results
            result = list(results)

            # Check if we got any results
            if not result:
                return jsonify({
                    'status': 'success',
                    'data': [],
                    'message': 'No data found for the specified range'
                }), 200

            return jsonify({
                'status': 'success',
                'data': result
            }), 200
        except Exception as e:
            return jsonify({
                'status': 'error',
                'err': str(e)
            })

    @staticmethod
    def get_youtube_video_index(artist_id, range):
        """
        get the latest 50 videos total views,
        & total likes, avg likes,
        & total comments, avg comments
        :return:
        total views, total likes, total comments,
        avg likes, avg comments
        """
        # Validate required parameters
        if not artist_id:
            return jsonify({'err': 'Missing artist_id parameter'}), 400
        if not range:
            return jsonify({'err': 'Missing range parameter'}), 400

        try:

            range_days = {
                "7d": 7,
                "28d": 28,
                "90d": 90,
                "180d": 180,
                "365d": 365
            }

            # Get number of days from range mapping, default to 7 days if range not found
            days = range_days.get(range, 7)

            pipeline = [
                {"$match": {
                    "channel_id": artist_id
                }},
                {"$sort": {"datetime": -1}},
                # match date range
                # {"$match": {
                #     "datetime": {
                #         "$lte": date_end,
                #         "$gt": seven_days_ago
                #     }
                # }},
                {"$limit": days},
                # unwind video
                {"$unwind": "$video"},
                {"$project": {
                    "_id": 0,
                    "datetime": {
                        "$dateToString": {
                            "format": "%Y-%m-%d",
                            "date": "$datetime"
                        }
                    },
                    "published_at": "$video.published_at",
                    "view_count": {"$toInt": "$video.view_count"},
                    "like_count": {"$toInt": "$video.like_count"},
                    "favorite_count": {"$toInt": "$video.favorite_count"},
                    "comment_count": {"$toInt": "$video.comment_count"}
                }},
                # group videos by date
                {"$group": {
                    "_id": "$datetime",
                    "video": {"$sum": {"$toInt": 1}},
                    "total_view": {"$sum": "$view_count"},
                    "total_like": {"$sum": "$like_count"},
                    "total_favorite": {"$sum": "$favorite_count"},
                    "total_comment": {"$sum": "$comment_count"}
                }},
                {"$sort": {"_id": 1}},
                # # calculate subtotal
                {"$addFields": {
                    "sub_total": {
                        "$sum": ["$total_like", "$total_favorite", "$total_comment"]
                    }
                }},
                # calculate engagement rate & avg
                {"$project": {
                    "_id": 0,
                    "datetime": "$_id",
                    "video": "$video",
                    "total_view": "$total_view",
                    "total_like": "$total_like",
                    "avg_like": {
                        "$divide": ["$total_like", "$video"]
                    },
                    "total_comment": "$total_comment",
                    "avg_comment": {
                            "$divide": ["$total_comment", "$video"]
                    },
                    "eng_rate": {
                            "$multiply": [{
                                "$divide": ["$sub_total", "$total_view"]
                            }, 100]
                    }
                }}
            ]

            results = Youtube.objects().aggregate(pipeline)

            # Format results
            result = list(results)  # Convert cursor to list

            # Check if we got any results
            if not result:
                return jsonify({
                    'status': 'success',
                    'data': [],
                    'message': 'No data found for the specified range'
                }), 200

            return jsonify({
                'status': 'success',
                'data': result
            }), 200
        except Exception as e:
            return jsonify({
                'status': 'error',
                'err': str(e)
            }), 500

    @staticmethod
    def get_youtube_channel_hashtag(artist_id, date_end, range):
        # Validate required parameters
        if not artist_id:
            return jsonify({'err': 'Missing artist_id parameter'}), 400
        if not date_end:
            return jsonify({'err': 'Missing date_end parameter'}), 400
        if not range:
            return jsonify({'err': 'Missing range parameter'}), 400

        try:
            # Validate and parse date
            format = "%Y-%m-%d"
            try:
                date_end = datetime.datetime.strptime(date_end, format)
            except ValueError:
                return jsonify({'err': 'Invalid date format. Use YYYY-MM-DD'}), 400

            # Define range mapping
            range_days = {
                "7d": 7,
                "28d": 28,
                "90d": 90,
                "180d": 180,
                "365d": 365
            }

            # Get number of days from range mapping, default to 7 days if range not found
            days = range_days.get(range, 7)
            start_date = date_end - datetime.timedelta(days=days)

            # mongodb pipeline
            pipeline = [
                # match artist channel id
                {"$match": {
                    "channel_id": artist_id
                }},
                {"$sort": {"datetime": 1}},
                # match date range
                {"$match": {
                    "datetime": {
                        "$lte": date_end,
                        "$gt": start_date
                    }
                }},
                {"$project": {
                    "_id": 0,
                    "datetime": {
                        "$dateToString": {
                            "format": "%Y-%m-%d",
                            "date": "$datetime"
                        }
                    },
                    "channel_hashtag": "$channel_hashtag",
                }}
            ]

            # Execute pipeline
            results = Youtube.objects().aggregate(pipeline)

            # Format results
            result = list(results)  # Convert cursor to list

            # Check if we got any results
            if not result:
                return jsonify({
                    'status': 'success',
                    'data': [],
                    'message': 'No data found for the specified range'
                }), 200

            return jsonify({
                'status': 'success',
                'data': result
            }), 200
        except Exception as e:
            return jsonify({
                'status': 'error',
                'err': str(e)
            }), 500

    @staticmethod
    def get_youtube_video_hashtag(artist_id, date_end, range):
        # Validate required parameters
        if not artist_id:
            return jsonify({'err': 'Missing artist_id parameter'}), 400
        if not date_end:
            return jsonify({'err': 'Missing date_end parameter'}), 400
        if not range:
            return jsonify({'err': 'Missing range parameter'}), 400

        try:
            # Validate and parse date
            format = "%Y-%m-%d"
            try:
                date_end = datetime.datetime.strptime(date_end, format)
            except ValueError:
                return jsonify({'err': 'Invalid date format. Use YYYY-MM-DD'}), 400

            # Define range mapping
            range_days = {
                "7d": 7,
                "28d": 28,
                "90d": 90,
                "180d": 180,
                "365d": 365
            }

            # Get number of days from range mapping, default to 7 days if range not found
            days = range_days.get(range, 7)
            start_date = date_end - datetime.timedelta(days=days)

            # mongodb pipeline
            pipeline = [
                # match artist channel id
                {"$match": {
                    "channel_id": artist_id
                }},
                {"$sort": {"datetime": 1}},
                # match date range
                {"$match": {
                    "datetime": {
                        "$lte": date_end,
                        "$gt": start_date
                    }
                }},
                {"$project": {
                    "_id": 0,
                    "datetime": {
                        "$dateToString": {
                            "format": "%Y-%m-%d",
                            "date": "$datetime"
                        }
                    },
                    "video_hashtag": "$video_hashtag"
                }}
            ]

            results = Youtube.objects().aggregate(pipeline)
            # Format results
            result = list(results)  # Convert cursor to list

            # Check if we got any results
            if not result:
                return jsonify({
                    'status': 'success',
                    'data': [],
                    'message': 'No data found for the specified range'
                }), 200

            return jsonify({
                'status': 'success',
                'data': result
            }), 200
        except Exception as e:
            return jsonify({
                'status': 'error',
                'err': str(e)
            }), 500

    @staticmethod
    def get_youtube_latest_video_info(artist_id):
        # Validate required parameters
        if not artist_id:
            return jsonify({'err': 'Missing artist_id parameter'}), 400

        try:
            pipeline = [
                {"$match": {
                    "channel_id": artist_id
                }},
                {"$sort": {"datetime": -1}},
                {"$limit": 1},
                {"$project": {
                    "_id": 0,
                    "datetime": "$datetime",
                    "channel_id": "$channel_id",
                    "video": "$video"
                }},
                {"$unwind": "$video"},
                {"$project": {
                    "_id": 0,
                    "datetime": "$datetime",
                    "channel_id": "$channel_id",
                    "published_at": "$video.publish_at",
                    "title": "$video.title",
                    "thumbnail": "$video.thumbnail",
                    "tags": "$video.tags",
                    "url": {
                        "$concat": [
                            "https://www.youtube.com/watch?v=", "$video.code", "/"
                        ]
                    },
                    "category_id": "$video.category_id",
                    "view_count": {"$toInt": "$video.view_count"},
                    "comment_count": {"$toInt": "$video.comment_count"},
                    "like_count": {"$toInt": "$video.like_count"},
                    "favorite_count": {"$toInt": "$video.favorite_count"},
                    "eng_rate": {
                        "$multiply": [
                            {"$divide": [
                                {"$sum": ["$video.like_count", "$video.comment_count"]}, {"$toInt": "$video.view_count"}
                            ]}, 100
                        ]
                    }
                }}
            ]

            results = Youtube.objects().aggregate(pipeline)
            result = list(results)

            if not result:
                return jsonify({
                    'status': 'success',
                    'data': [],
                    'message': 'No data found for the specified id'
                }), 200

            return jsonify({
                'status': 'success',
                'data': result
            }), 200

        except Exception as e:
            return jsonify({
                'status': 'error',
                'err': str(e)
            })
