from models.sns.instagram_model import Instagram, InstagramLatest
import datetime
from flask import jsonify, request


class InstagramController:
    @staticmethod
    def get_follower(artist_id, date_end, range):
        """
           Get Instagram follower count data for a specific time range
        :param artist_id: The ID of the artist to get follower data for
        :param date_end: The end date for the data range in format 'YYYY-MM-DD'
        :param range: The time range to analyze ('7d', '28d', '90d', '180d', '365d')
        :return: JSON response containing follower data with dates and counts
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

            # Construct MongoDB pipeline
            pipeline = [
                # Match artist and date range
                {"$match": {
                    "$and": [
                        {"user_id": artist_id},
                        {
                            "datetime": {
                                "$lte": date_end,
                                "$gt": start_date
                            }
                        }
                    ]
                }},
                # Sort by datetime for consistent results
                {"$sort": {"datetime": 1}},
                # Project required fields
                {"$project": {
                    "_id": 0,
                    "datetime": {
                        "$dateToString": {
                            "format": format,
                            "date": "$datetime"
                        }
                    },
                    "follower": "$follower_count"
                }}
            ]

            # Execute pipeline
            results = Instagram.objects().aggregate(pipeline)

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
    def get_post_count(artist_id, date_end, range):
        """
         Get Instagram media counts for a specific time range
        :param artist_id: The ID of the artist to get post data for
        :param date_end: The end date for the data range in format 'YYYY-MM-DD'
        :param range: The time range to analyze ('7d', '28d', '90d', '180d', '365d')
        :return: JSON response containing post count data with dates and counts
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

            # Construct MongoDB pipeline
            pipeline = [
                # Match artist and date range
                {"$match": {
                    "$and": [
                        {"user_id": artist_id},
                        {
                            "datetime": {
                                "$lte": date_end,
                                "$gt": start_date
                            }
                        }
                    ]
                }},
                # Sort by datetime for consistent results
                {"$sort": {"datetime": 1}},
                # Project required fields
                {"$project": {
                    "_id": 0,
                    "datetime": {
                        "$dateToString": {
                            "format": format,
                            "date": "$datetime"
                        }
                    },
                    "posts_count": "$media_count"
                }}
            ]

            # Execute pipeline
            results = Instagram.objects().aggregate(pipeline)

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
    def get_threads_follower(artist_id, date_end, range):
        """
Get Instagram threads follower count data for a specific time range
        :param artist_id: The ID of the artist to get threads follower data for
        :param date_end: The end date for the data range in format 'YYYY-MM-DD'
        :param range: The time range to analyze ('7d', '28d', '90d', '180d', '365d')
        :return: JSON response containing threads follower data with dates and counts
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

            # Construct MongoDB pipeline
            pipeline = [
                # Match artist and date range
                {"$match": {
                    "$and": [
                        {"user_id": artist_id},
                        {
                            "datetime": {
                                "$lte": date_end,
                                "$gt": start_date
                            }
                        }
                    ]
                }},
                # Sort by datetime for consistent results
                {"$sort": {"datetime": 1}},
                # Project required fields
                {"$project": {
                    "_id": 0,
                    "datetime": {
                        "$dateToString": {
                            "format": format,
                            "date": "$datetime"
                        }
                    },
                    "threads_follower": "$threads_follower"
                }}
            ]

            # Execute pipeline
            results = Instagram.objects().aggregate(pipeline)

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
    def get_likes(artist_id, range):
        """
        Get total likes and likes per post for the latest posts within a specified time range
        :param artist_id: The ID of the artist to get like data for
        :param range: The time range to analyze ('7d', '28d', '90d', '180d', '365d')
        :return: JSON response containing like data with dates, total likes, and likes per post
        """
        # Validate required parameters
        if not artist_id:
            return jsonify({'err': 'Missing artist_id parameter'}), 400
        if not range:
            return jsonify({'err': 'Missing range parameter'}), 400

        try:
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

            # Construct MongoDB pipeline
            pipeline = [
                # Match artist
                {"$match": {
                    "user_id": artist_id
                }},
                # Sort by datetime for consistent results
                {"$sort": {"datetime": 1}},
                # Limit to specified number of days
                {"$limit": days},
                # Unwind posts array to work with individual posts
                {"$unwind": "$posts"},
                # Project required fields
                {"$project": {
                    "_id": 0,
                    "datetime": {
                        "$dateToString": {
                            "format": "%Y-%m-%d",
                            "date": "$datetime"
                        }
                    },
                    "code": "$posts.code",
                    "like_count": "$posts.like_count"
                }},
                # Group by date to calculate daily totals
                {"$group": {
                    "_id": "$datetime",
                    "code_list": {"$push": "$code"},
                    "post_count": {"$sum": 1},
                    "total_like": {"$sum": "$like_count"}
                }},
                # Calculate likes per post and format final output
                {"$project": {
                    "_id": 0,
                    "datetime": "$_id",
                    "total_likes": "$total_like",
                    "like_per_post": {
                        "$round": [
                            {"$divide": ["$total_like", "$post_count"]}, 2
                        ]
                    }
                }}
            ]

            # Execute pipeline
            results = Instagram.objects().aggregate(pipeline)

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
    def get_comments(artist_id, range):
        """
        Get total comments and comments per post for the latest posts within a specified time range
        :param artist_id: The ID of the artist to get like data for
        :param range: The time range to analyze ('7d', '28d', '90d', '180d', '365d')
        :return: JSON response containing like data with dates, total likes, and likes per post
        """
        # Validate required parameters
        if not artist_id:
            return jsonify({'err': 'Missing artist_id parameter'}), 400
        if not range:
            return jsonify({'err': 'Missing range parameter'}), 400

        try:
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

            pipeline = [
                {"$match": {
                    "user_id": artist_id
                }},
                # sort by datetime
                {"$sort": {"datetime": 1}},
                # limit posts
                {"$limit": days},
                {"$unwind": "$posts"},
                # return comment fields
                {"$project": {
                    "_id": 0,
                    "datetime": {
                        "$dateToString": {
                            "format": "%Y-%m-%d",
                            "date": "$datetime"
                        }
                    },
                    "code": "$posts.code",
                    "comment_count": "$posts.comment_count"
                }},
                # group by date,
                # to calculate the total likes of latest 12 posts daily
                {"$group": {
                    "_id": "$datetime",
                    "code_list": {"$push": "$code"},
                    "post_count": {"$sum": 1},
                    "total_comment": {"$sum": "$comment_count"}
                }},
                # get comments per post
                {"$project": {
                    "_id": 0,
                    "datetime": "$_id",
                    "total_comments": "$total_comment",
                    "comment_per_post": {
                        "$round": [
                            {"$divide": ["$total_comment", "$post_count"]}, 2
                        ]
                    }
                }}
            ]

            # Execute pipeline
            results = Instagram.objects().aggregate(pipeline)

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
    def get_posts_index(artist_id):
        """
        get instagram latest 12 posts index
        :param: artist_id
        :return:
        """
        # Validate required parameters
        if not artist_id:
            return jsonify({'err': 'Missing artist_id parameter'}), 400

        try:
            pipeline = [
            # match artist
            {"$match": {
                "user_id": artist_id
            }},
            # sort by datetime
            {"$sort": {"datetime": -1}},
            {"$limit": 1},
            {"$unwind": "$posts"},
            # project
            {"$project": {
                "_id": 0,
                "datetime": "$datetime",
                "user_id": "$user_id",
                "pk": "$posts.pk",
                "username": "$posts.username",
                "code": "$posts.code",
                "taken_at": "$posts.taken_at",
                "media_type": "$posts.media_type",
                "product_type": "$posts.product_type",
                "comment_count": "$posts.comment_count",
                "like_count": "$posts.like_count",
                "play_count": "$posts.play_count",
                "view_count": "$posts.view_count",
                "caption_text": "$posts.caption_text",
                "thumbnail": "$posts.thumbnail",
                "video_url": "$posts.video_url"
            }},
            # lookup artist follower Number(
            {"$lookup": {
                "from": "instagram",
                "as": "ig_info",
                "let": {"user_idd": "$user_id"},
                "pipeline": [
                    {"$match": {
                        "$expr": {
                            "$eq": ["$user_id", "$$user_idd"]
                        }
                    }},
                    {"$sort": {"datetime": -1}},
                    {"$limit": 1}
                ]
            }},
            # unwind  ig_info
            {"$unwind": "$ig_info"},
            # project
            {"$project": {
                "_id": 0,
                "datetime": "$datetime",
                "user_id": "$user_id",
                "username": "$username",
                "taken_at": "$taken_at",
                "media_type": "$media_type",
                "product_type": "$product_type",
                "comment_count": "$comment_count",
                "like_count": "$like_count",
                "play_count": "$play_count",
                # "view_count": "$view_count",
                "caption_text": "$caption_text",
                "thumbnail": "$thumbnail",
                # "follower": "$ig_info.follower_count",
                "engagement_rate": {
                    "$round": [{
                        "$divide": [
                            {"$sum": ["$like_count", "$comment_count"]}, "$ig_info.follower_count"
                        ]}, 3]
                },
                "url": {
                    "$concat": [
                        "https://instagram.com/p/", "$code", "/"
                    ]
                }
            }}
        ]

            results = Instagram.objects().aggregate(pipeline)

            result = list(results)

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
    def get_hashtags_most_engaged_recent_twelve(artist_id):
        if not artist_id:
            return jsonify({'err': 'Missing required parameters'}), 400

        try:
            pipeline = [
            {"$match": {
                "user_id": artist_id
            }},
            {"$sort": {"datetime": -1}},
            {"$limit": 1},
            # lookup artist follower
            {"$lookup": {
                "from": "instagram",
                "as": "ig_info",
                "let": {"user_idd": "$user_id"},
                "pipeline": [
                    {"$match": {
                        "$expr": {
                            "$eq": ["$user_id", "$$user_idd"]
                        }
                    }},
                    {"$sort": {"datetime": -1}},
                    {"$limit": 1}
                ]
            }},
            {"$unwind": "$ig_info"},
            {"$unwind": "$posts"},
            {"$project": {
                "_id": 0,

                "hashtag": "$posts.hashtag",
                "eng_rate": {
                    "$round": [{
                        "$multiply": [
                            {"$divide": [
                                {"$sum": ["$posts.like_count", "$posts.comment_count"]}, "$ig_info.follower_count"
                            ]}, 100
                        ]
                    }, 3]
                }
            }},
            {"$unwind": "$hashtag"},
            {"$group": {
                "_id": "$hashtag",
                "count": {"$sum": 1},
                "eng_rate": {"$sum": "$eng_rate"}
            }},
            {"$project": {
                "_id": 0,
                "tag": "$_id",
                "eng_rate_per_hashtag": {
                    "$round": [
                        {"$divide": ["$eng_rate", "$count"]}, 3
                    ]
                }
            }},
            {"$sort": {"eng_rate_per_hashtag": -1}},
            {"$limit": 10}
        ]

            results = InstagramLatest.objects().aggregate(pipeline)

            result = list(results)

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
    def get_hashtags_most_used_recent_twelve(artist_id):
        if not artist_id:
            return jsonify({'err': 'Missing required parameters'}), 400

        try:
            pipeline = [
            {"$match": {
                "user_id": artist_id
            }},
            {"$sort": {"datetime": -1}},
            {"$limit": 1},
            # lookup artist follower
            {"$lookup": {
                "from": "instagram",
                "as": "ig_info",
                "let": {"user_idd": "$user_id"},
                "pipeline": [
                    {"$match": {
                        "$expr": {
                            "$eq": ["$user_id", "$$user_idd"]
                        }
                    }},
                    {"$sort": {"datetime": -1}},
                    {"$limit": 1}
                ]
            }},
            {"$unwind": "$ig_info"},
            {"$unwind": "$posts"},
            {"$project": {
                "_id": 0,
                "hashtag": "$posts.hashtag"
            }},
            {"$unwind": "$hashtag"},
            {"$group": {
                "_id": "$hashtag",
                "count": {"$sum": 1},

            }},
            {"$project": {
                "_id": 0,
                "tag": "$_id",
                "count": {"$toInt": "$count"}
            }},
            {"$sort": {"count": -1}},
            {"$limit": 10}
        ]

            results = InstagramLatest.objects().aggregate(pipeline)

            result = list(results)

            return jsonify({
                'status': 'success',
                'data': result
            }), 200
        except Exception as e:
            return jsonify({
                'status': 'error',
                'err': str(e)
            }), 500
