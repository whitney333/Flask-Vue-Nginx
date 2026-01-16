from models.sns.youtube_model import YoutubeVideo, Youtube
from models.artist_model import Artists
from models.user_model import Users
import pandas as pd
import numpy as np
import datetime
from flask import jsonify, request, g
from services.youtube_service import YoutubeService
from libs.utils import get_current_user


class YoutubeController:
    @staticmethod
    # get channel id by artist id
    def get_artist_by_mid(artist_id):
        # Validate required parameters
        if not artist_id:
            return jsonify({'err': 'Missing artist_id parameter'}), 400
        try:
            pipeline = [
                {"$match": {
                    # match artist mid
                    'artist_id': artist_id
                }},
                {"$project": {
                    "_id": 0
                }}
            ]

            results = Artists.objects().aggregate(pipeline)

            result = list(results)

            return result

        except Exception as e:
            return jsonify({
                'status': 'error',
                'err': str(e)
            }), 500

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

    ########### v2 endpoint ###########
    def get_youtube_channel_basic_by_artist_id(artist_id):
        # get logged in user
        user = Users.objects(firebase_id=g.firebase_id).first()

        if not user:
            return jsonify({
                "error": "User not found"
            }), 404

        # check if user follows this artist
        matched_artist = None
        for artist in user.followed_artist:
            # check if passed artist_id is inside
            if artist.artist_id == artist_id:
                matched_artist = artist
                break

        if not matched_artist:
            return jsonify({
                "error": "You are not following this artist"
            }), 403

        # query youtube data
        # data range
        date_end = request.args.get("start")
        range_str = request.args.get("filter")
        if not date_end or not range_str:
            return jsonify({
                "error": "Missing start date or range"
            }), 400

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
            days = range_days.get(range_str, 7)
            start_date = date_end - datetime.timedelta(days=days)

        except ValueError:
            return jsonify({
                "error": "Invalid date format"
            }), 400

        # youtube_data = Youtube.objects(artist=matched_artist).first()
        youtube_data = Youtube.objects(
            channel_id=matched_artist.youtube_id,
            datetime__gte=start_date,
            datetime__lte=date_end
        ).order_by("datetime")

        if not youtube_data:
            return jsonify({
                "error": "No youtube data found"
            }), 404

        result = []
        for y in youtube_data:
            result.append({
                "datetime": y.datetime,
                "channel_id": y.channel_id,
                "view_count": y.view_count,
                "subscriber_count": y.subscriber_count,
                "video_count": y.video_count,
                "channel_hashtag": y.channel_hashtag,
                "video_hashtag": y.video_hashtag
            })

        return jsonify({
            "status": "success",
            "data": result
        }), 200

    def get_youtube_channel_view_by_artist_id(artist_id):
        # get logged in user
        user = Users.objects(firebase_id=g.firebase_id).first()

        if not user:
            return jsonify({
                "error": "User not found"
            }), 404

        # check if user follows this artist
        matched_artist = None
        for artist in user.followed_artist:
            # check if passed artist_id is inside
            if artist.artist_id == artist_id:
                matched_artist = artist
                break

        if not matched_artist:
            return jsonify({
                "error": "You are not following this artist"
            }), 403

        # data range
        date_end = request.args.get("start")
        range_str = request.args.get("filter")
        if not date_end or not range_str:
            return jsonify({
                "error": "Missing start date or range"
            }), 400

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
            days = range_days.get(range_str, 7)
            start_date = date_end - datetime.timedelta(days=days)

        except ValueError:
            return jsonify({
                "error": "Invalid date format"
            }), 400

        try:
            youtube_data = Youtube.objects(
                channel_id=matched_artist.youtube_id,
                datetime__gte=start_date,
                datetime__lte=date_end
            ).order_by("datetime")

            if not youtube_data:
                return jsonify({
                    "error": "No youtube data found"
                }), 404

            result = []
            for y in youtube_data:
                result.append({
                    "datetime": y.datetime,
                    "channel_id": y.channel_id,
                    "view_count": y.view_count,
                })

            return jsonify({
                "status": "success",
                "data": result
            }), 200
        except Exception as e:
            return jsonify({
                "status": "error",
                "error": str(e)
            }), 500

    def get_youtube_video_view_by_artist_id(artist_id):
        # get logged in user
        user = Users.objects(firebase_id="01N9AQsbhEf1XcQbTSqPynzNfXA3").first()

        if not user:
            return jsonify({
                "error": "User not found"
            }), 404

        # check if user follows this artist
        matched_artist = None
        for artist in user.followed_artist:
            # check if passed artist_id is inside
            if artist.artist_id == artist_id:
                matched_artist = artist
                break

        if not matched_artist:
            return jsonify({
                "error": "You are not following this artist"
            }), 403

        # data range
        date_end = request.args.get("start")
        range_str = request.args.get("filter")
        if not date_end or not range_str:
            return jsonify({
                "error": "Missing start date or range"
            }), 400

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
            days = range_days.get(range_str, 7)
            start_date = date_end - datetime.timedelta(days=days)

        except ValueError:
            return jsonify({
                "error": "Invalid date format"
            }), 400

        try:
            pipeline = [
                {"$match": {
                    "channel_id": matched_artist.youtube_id
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
            youtube_data = Youtube.objects().aggregate(pipeline)

            if not youtube_data:
                return jsonify({
                    "error": "No youtube data found"
                }), 404

            # Format results
            result = list(youtube_data)

            return jsonify({
                "status": "success",
                "data": result
            }), 200
        except Exception as e:
            return jsonify({
                "status": "error",
                "error": str(e)
            }), 500

    def get_youtube_video_index_by_artist_id(artist_id):
        # get logged in user
        user = Users.objects(firebase_id="01N9AQsbhEf1XcQbTSqPynzNfXA3").first()

        if not user:
            return jsonify({
                "error": "User not found"
            }), 404

        # check if user follows this artist
        matched_artist = None
        for artist in user.followed_artist:
            # check if passed artist_id is inside
            if artist.artist_id == artist_id:
                matched_artist = artist
                break

        if not matched_artist:
            return jsonify({
                "error": "You are not following this artist"
            }), 403

        # data range
        date_end = request.args.get("start")
        range_str = request.args.get("filter")
        if not date_end or not range_str:
            return jsonify({
                "error": "Missing start date or range"
            }), 400

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
            days = range_days.get(range_str, 7)
            start_date = date_end - datetime.timedelta(days=days)

        except ValueError:
            return jsonify({
                "error": "Invalid date format"
            }), 400

        try:
            pipeline = [
                {"$match": {
                    "channel_id": matched_artist.youtube_id
                }},
                {"$sort": {"datetime": -1}},
                {"$limit": days},
                # match date range
                {"$match": {
                    "datetime": {
                        "$lte": date_end,
                        "$gt": start_date
                    }
                }},
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
                    # "eng_rate": {
                    #         "$multiply": [{
                    #             "$divide": ["$sub_total", "$total_view"]
                    #         }, 100]
                    # }
                }}
            ]
            youtube_data = Youtube.objects().aggregate(pipeline)

            # Format results
            result = list(youtube_data)

            if not youtube_data:
                return jsonify({
                    "status": "success",
                    "data": [],
                    "message": "No data found for the specified range"
                }), 200

            return jsonify({
                "status": "success",
                "data": result
            }), 200
        except Exception as e:
            return jsonify({
                "error": str(e)
            }), 500

    def get_youtube_latest_video_info_by_artist_id(artist_id):
        # get logged in user
        user = Users.objects(firebase_id=g.firebase_id).first()

        if not user:
            return jsonify({
                "error": "User not found"
            }), 404

        # check if user follows this artist
        matched_artist = None
        for artist in user.followed_artist:
            # check if passed artist_id is inside
            if artist.artist_id == artist_id:
                matched_artist = artist
                break

        if not matched_artist:
            return jsonify({
                "error": "You are not following this artist"
            }), 403

        try:
            pipeline = [
                {"$match": {
                    "channel_id": matched_artist.youtube_id
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
                    "published_at": "$video.published_at",
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

            youtube_data = Youtube.objects().aggregate(pipeline)

            if not youtube_data:
                return jsonify({
                    'status': 'success',
                    'data': [],
                    'message': 'No data found for the specified artist id'
                }), 200

            result = list(youtube_data)

            return jsonify({
                'status': 'success',
                'data': result
            }), 200
        except Exception as e:
            return jsonify({
                "error": str(e)
            })

    ####### NEW #######
    @staticmethod
    def get_youtube_follower_growth(artist_id, campaign_start):
        if not artist_id or not campaign_start:
            return jsonify({
                "err": "Missing required parameters"
            }), 400

        try:
            campaign_start_dt = datetime.datetime.strptime(campaign_start, "%Y-%m-%d")
            result = YoutubeService.get_follower_growth(artist_id, campaign_start_dt)

            if not result:
                return jsonify({
                    "status": "success",
                    "data": None,
                    "message": "Insufficient data"
                }), 200
            return jsonify({
                "status": "success",
                "data": result
            }), 200

        except ValueError as ve:
            return jsonify({
                "err": str(ve)
            }), 400

        except Exception as e:
            return jsonify({
                "status": "error",
                "err": str(e)
            }), 500

    @staticmethod
    def get_youtube_channel_hashtag_growth(artist_id, campaign_start):
        if not artist_id or not campaign_start:
            return jsonify({
                "err": "Missing required parameters"
            }), 400

        try:
            campaign_start_dt = datetime.datetime.strptime(campaign_start, "%Y-%m-%d")
            result = YoutubeService.get_channel_hashtag_growth(artist_id, campaign_start_dt)

            if not result:
                return jsonify({
                    "status": "success",
                    "data": None,
                    "message": "Insufficient data"
                }), 200
            return jsonify({
                "status": "success",
                "data": result
            }), 200

        except ValueError as ve:
            return jsonify({
                "err": str(ve)
            }), 400

        except Exception as e:
            return jsonify({
                "status": "error",
                "err": str(e)
            }), 500

    @staticmethod
    def get_youtube_video_hashtag_growth(artist_id, campaign_start):
        if not artist_id or not campaign_start:
            return jsonify({
                "err": "Missing required parameters"
            }), 400

        try:
            campaign_start_dt = datetime.datetime.strptime(campaign_start, "%Y-%m-%d")
            result = YoutubeService.get_video_hashtag_growth(artist_id, campaign_start_dt)

            if not result:
                return jsonify({
                    "status": "success",
                    "data": None,
                    "message": "Insufficient data"
                }), 200
            return jsonify({
                "status": "success",
                "data": result
            }), 200

        except ValueError as ve:
            return jsonify({
                "err": str(ve)
            }), 400

        except Exception as e:
            return jsonify({
                "status": "error",
                "err": str(e)
            }), 500

    @staticmethod
    def get_youtube_engagement_growth(artist_id, campaign_start):
        if not artist_id or not campaign_start:
            return jsonify({
                "err": "Missing required parameters"
            }), 400

        try:
            campaign_start_dt = datetime.datetime.strptime(campaign_start, "%Y-%m-%d")
            result = YoutubeService.get_engagement_growth(artist_id, campaign_start_dt)

            if not result:
                return jsonify({
                    "status": "success",
                    "data": None,
                    "message": "Insufficient data"
                }), 200
            return jsonify({
                "status": "success",
                "data": result
            }), 200

        except ValueError as ve:
            return jsonify({
                "err": str(ve)
            }), 400

        except Exception as e:
            return jsonify({
                "status": "error",
                "err": str(e)
            }), 500

    @staticmethod
    def get_youtube_follower(artist_id, date_end, range):
        # validate
        if not artist_id or not date_end or not range:
            return jsonify({
                "err": "Missing required parameters"
            }), 400

        try:
            date_end = datetime.datetime.strptime(date_end, "%Y-%m-%d")
        except ValueError:
            return jsonify({
                "err": "Invalid date format. Use YYYY-MM-DD"
            }), 400

        # get user
        user = get_current_user(optional=True)
        # print("headers:", dict(request.headers))
        # print("cookies:", request.cookies)
        # print("user:", user)
        try:
            result = YoutubeService.get_chart_follower(
                user=user,
                artist_id=artist_id,
                date_end=date_end,
                range_key=range
            )
        except ValueError as e:
            return jsonify({"err": str(e)}), 404

        # response
        if result.get("locked"):
            return jsonify({
                "status": "locked",
                "data": [],
                "meta": {
                    "allowed_ranges": result["allowed_ranges"],
                    "is_premium": bool(user and user.is_premium)
                }
            }), 200

        return jsonify({
            "status": "success",
            "data": result["data"],
            "meta": result["meta"]
        }), 200

    @staticmethod
    def get_youtube_total_video_view(artist_id, date_end, range):
        # validate
        if not artist_id or not date_end or not range:
            return jsonify({
                "err": "Missing required parameters"
            }), 400

        try:
            date_end = datetime.datetime.strptime(date_end, "%Y-%m-%d")
        except ValueError:
            return jsonify({
                "err": "Invalid date format. Use YYYY-MM-DD"
            }), 400

        # get user
        user = get_current_user(optional=True)

        try:
            result = YoutubeService.get_chart_video_view(
                user=user,
                artist_id=artist_id,
                date_end=date_end,
                range_key=range
            )
        except ValueError as e:
            return jsonify({"err": str(e)}), 404

        # response
        if result.get("locked"):
            return jsonify({
                "status": "locked",
                "data": [],
                "meta": {
                    "allowed_ranges": result["allowed_ranges"],
                    "is_premium": bool(user and user.is_premium)
                }
            }), 200

        return jsonify({
            "status": "success",
            "data": result["data"],
            "meta": result["meta"]
        }), 200

    @staticmethod
    def get_youtube_latest_video_like_and_comment(artist_id, date_end, range):
        # validate
        if not artist_id or not date_end or not range:
            return jsonify({
                "err": "Missing required parameters"
            }), 400

        try:
            date_end = datetime.datetime.strptime(date_end, "%Y-%m-%d")
        except ValueError:
            return jsonify({
                "err": "Invalid date format. Use YYYY-MM-DD"
            }), 400

        # get user
        user = get_current_user(optional=True)

        try:
            result = YoutubeService.get_chart_video_likes_and_comments(
                user=user,
                artist_id=artist_id,
                date_end=date_end,
                range_key=range
            )
        except ValueError as e:
            return jsonify({"err": str(e)}), 404

        # response
        if result.get("locked"):
            return jsonify({
                "status": "locked",
                "data": [],
                "meta": {
                    "allowed_ranges": result["allowed_ranges"],
                    "is_premium": bool(user and user.is_premium)
                }
            }), 200

        return jsonify({
            "status": "success",
            "data": result["data"],
            "meta": result["meta"]
        }), 200

    @staticmethod
    def get_youtube_most_used_hashtag(artist_id, range_key):
        # get user info
        user = get_current_user(optional=True)

        # normalize range
        range_key = str(range_key) if range_key else "5"

        try:
            data = YoutubeService.get_chart_most_used_hashtag(
                user=user,
                artist_id=artist_id,
                range_key=range_key
            )

            return jsonify({
                "status": "success",
                "data": data
            }), 200

        except PermissionError as e:
            return jsonify({
                "error": str(e)
            }), 403

        except Exception as e:
            return jsonify({
                "error": str(e)
            }), 500

    @staticmethod
    def get_youtube_most_engaged_hashtag(artist_id, range_key):
        # get user info
        user = get_current_user(optional=True)

        # normalize range
        range_key = str(range_key) if range_key else "5"

        try:
            data = YoutubeService.get_chart_most_engaged_hashtag(
                user=user,
                artist_id=artist_id,
                range_key=range_key
            )

            return jsonify({
                "status": "success",
                "data": data
            }), 200

        except PermissionError as e:
            return jsonify({
                "error": str(e)
            }), 403

        except Exception as e:
            return jsonify({
                "error": str(e)
            }), 500

    @staticmethod
    def get_youtube_latest_videos(artist_id):
        # get user info
        user = get_current_user(optional=True)

        try:
            data = YoutubeService.get_posts(
                artist_id=artist_id
            )

            return jsonify({
                "status": "success",
                "data": data
            }), 200

        except PermissionError as e:
            return jsonify({
                "error": str(e)
            }), 403

        except Exception as e:
            return jsonify({
                "error": str(e)
            }), 500
