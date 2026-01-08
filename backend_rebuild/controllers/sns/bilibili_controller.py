from models.sns.bilibili_model import Bilibili
from models.artist_model import Artists
import datetime
from flask import jsonify, request
from services.bilibili_service import BilibiliService


class BilibiliController:
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
    def get_follower(artist_id, date_end, range):
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
            # first get artist mid, then query spotify data
            # Check artist's MID, call method: get_artist_by_mid
            artists = BilibiliController.get_artist_by_mid(artist_id)
            artist = list(artists)

            # retrieve youtube id
            new_artist_id = artist[0]['bilibili_id']

            pipeline = [
                {"$match": {
                    "user_id": new_artist_id,
                }},
                {"$sort": {"datetime": 1}},
                {"$match": {
                    "datetime": {
                        "$lte": date_end,
                        "$gt": start_date
                    }
                }},
                {"$sort": {"datetime": 1}},
                {"$project": {
                    "_id": 0,
                    "datetime": {
                        "$dateToString": {
                            "format": format,
                            "date": "$datetime"
                    }},
                    "id": "$user_id",
                    "follower": "$follower"
                }},
            ]

            results = Bilibili.objects().aggregate(pipeline)
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
    def get_view(artist_id, date_end, range):
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
            # first get artist mid, then query spotify data
            # Check artist's MID, call method: get_artist_by_mid
            artists = BilibiliController.get_artist_by_mid(artist_id)
            artist = list(artists)

            # retrieve youtube id
            new_artist_id = artist[0]['bilibili_id']

            pipeline = [
                {"$match": {
                    "user_id": new_artist_id,
                }},
                {"$sort": {"datetime": 1}},
                {"$match": {
                    "datetime": {
                        "$lte": date_end,
                        "$gt": start_date
                    }
                }},
                {"$unwind": "$data"},
                {"$group": {
                    "_id": "$datetime",
                    "user_id": {"$first": "$user_id"},
                    "count": {"$sum": {"$toInt": 1}},
                    "total_view": {"$sum": "$data.view"}
                }},
                {"$sort": {"_id": 1}},
                {"$project": {
                    "_id": 0,
                    "datetime": {
                        "$dateToString": {
                            "format": format,
                            "date": "$_id"
                        }},
                    "id": "$user_id",
                    "total_view": "$total_view",
                    "avg_view": {
                        "$divide": [
                            "$total_view", "$count"
                        ]
                    }
                }}
            ]

            results = Bilibili.objects().aggregate(pipeline)
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
    def get_like(artist_id, date_end, range):
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
            # first get artist mid, then query spotify data
            # Check artist's MID, call method: get_artist_by_mid
            artists = BilibiliController.get_artist_by_mid(artist_id)
            artist = list(artists)

            # retrieve youtube id
            new_artist_id = artist[0]['bilibili_id']

            pipeline = [
                {"$match": {
                    "user_id": new_artist_id,
                }},
                {"$sort": {"datetime": 1}},
                {"$match": {
                    "datetime": {
                        "$lte": date_end,
                        "$gt": start_date
                    }
                }},
                {"$unwind": "$data"},
                {"$group": {
                    "_id": "$datetime",
                    "user_id": {"$first": "$user_id"},
                    "count": {"$sum": {"$toInt": 1}},
                    "total_like": {"$sum": "$data.like"}
                }},
                {"$sort": {"_id": 1}},
                {"$project": {
                    "_id": 0,
                    "datetime": {
                        "$dateToString": {
                            "format": format,
                            "date": "$_id"
                        }},
                    "id": "$user_id",
                    "total_like": "$total_like",
                    "avg_like": {
                        "$divide": [
                            "$total_like", "$count"
                        ]
                    }
                }}
            ]

            results = Bilibili.objects().aggregate(pipeline)
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
    def get_comment(artist_id, date_end, range):
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
            # first get artist mid, then query spotify data
            # Check artist's MID, call method: get_artist_by_mid
            artists = BilibiliController.get_artist_by_mid(artist_id)
            artist = list(artists)

            # retrieve youtube id
            new_artist_id = artist[0]['bilibili_id']

            pipeline = [
                {"$match": {
                    "user_id": new_artist_id,
                }},
                {"$sort": {"datetime": 1}},
                {"$match": {
                    "datetime": {
                        "$lte": date_end,
                        "$gt": start_date
                    }
                }},
                {"$unwind": "$data"},
                {"$group": {
                    "_id": "$datetime",
                    "user_id": {"$first": "$user_id"},
                    "count": {"$sum": {"$toInt": 1}},
                    "total_comment": {"$sum": "$data.comment"}
                }},
                {"$sort": {"_id": 1}},
                {"$project": {
                    "_id": 0,
                    "datetime": {
                        "$dateToString": {
                            "format": format,
                            "date": "$_id"
                        }},
                    "id": "$user_id",
                    "total_comment": "$total_comment",
                    "avg_comment": {
                        "$divide": [
                            "$total_comment", "$count"
                        ]
                    }
                }}
            ]

            results = Bilibili.objects().aggregate(pipeline)
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
    def get_share(artist_id, date_end, range):
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
            # first get artist mid, then query spotify data
            # Check artist's MID, call method: get_artist_by_mid
            artists = BilibiliController.get_artist_by_mid(artist_id)
            artist = list(artists)

            # retrieve youtube id
            new_artist_id = artist[0]['bilibili_id']

            pipeline = [
                {"$match": {
                    "user_id": new_artist_id,
                }},
                {"$sort": {"datetime": 1}},
                {"$match": {
                    "datetime": {
                        "$lte": date_end,
                        "$gt": start_date
                    }
                }},
                {"$unwind": "$data"},
                {"$group": {
                    "_id": "$datetime",
                    "user_id": {"$first": "$user_id"},
                    "count": {"$sum": {"$toInt": 1}},
                    "total_share": {"$sum": "$data.share"}
                }},
                {"$sort": {"_id": 1}},
                {"$project": {
                    "_id": 0,
                    "datetime": {
                        "$dateToString": {
                            "format": format,
                            "date": "$_id"
                        }},
                    "id": "$user_id",
                    "total_share": "$total_share",
                    "avg_share": {
                        "$divide": [
                            "$total_share", "$count"
                        ]
                    }
                }}
            ]

            results = Bilibili.objects().aggregate(pipeline)
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
    def get_bullet_chat(artist_id, date_end, range):
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
            # first get artist mid, then query spotify data
            # Check artist's MID, call method: get_artist_by_mid
            artists = BilibiliController.get_artist_by_mid(artist_id)
            artist = list(artists)

            # retrieve youtube id
            new_artist_id = artist[0]['bilibili_id']

            pipeline = [
                {"$match": {
                    "user_id": new_artist_id,
                }},
                {"$sort": {"datetime": 1}},
                {"$match": {
                    "datetime": {
                        "$lte": date_end,
                        "$gt": start_date
                    }
                }},
                {"$unwind": "$data"},
                {"$group": {
                    "_id": "$datetime",
                    "user_id": {"$first": "$user_id"},
                    "count": {"$sum": {"$toInt": 1}},
                    "total_danmu": {"$sum": "$data.danmu"}
                }},
                {"$sort": {"_id": 1}},
                {"$project": {
                    "_id": 0,
                    "datetime": {
                        "$dateToString": {
                            "format": format,
                            "date": "$_id"
                        }},
                    "id": "$user_id",
                    "total_danmu": "$total_danmu",
                    "avg_danmu": {
                        "$divide": [
                            "$total_danmu", "$count"
                        ]
                    }
                }}
            ]

            results = Bilibili.objects().aggregate(pipeline)
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
    def get_coin(artist_id, date_end, range):
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
            # first get artist mid, then query spotify data
            # Check artist's MID, call method: get_artist_by_mid
            artists = BilibiliController.get_artist_by_mid(artist_id)
            artist = list(artists)

            # retrieve youtube id
            new_artist_id = artist[0]['bilibili_id']

            pipeline = [
                {"$match": {
                    "user_id": new_artist_id,
                }},
                {"$sort": {"datetime": 1}},
                {"$match": {
                    "datetime": {
                        "$lte": date_end,
                        "$gt": start_date
                    }
                }},
                {"$unwind": "$data"},
                {"$group": {
                    "_id": "$datetime",
                    "user_id": {"$first": "$user_id"},
                    "count": {"$sum": {"$toInt": 1}},
                    "total_coin": {"$sum": "$data.coin"}
                }},
                {"$sort": {"_id": 1}},
                {"$project": {
                    "_id": 0,
                    "datetime": {
                        "$dateToString": {
                            "format": format,
                            "date": "$_id"
                        }},
                    "id": "$user_id",
                    "total_coin": "$total_coin",
                    "avg_coin": {
                        "$divide": [
                            "$total_coin", "$count"
                        ]
                    }
                }}
            ]

            results = Bilibili.objects().aggregate(pipeline)
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
    def get_collect(artist_id, date_end, range):
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
            # first get artist mid, then query spotify data
            # Check artist's MID, call method: get_artist_by_mid
            artists = BilibiliController.get_artist_by_mid(artist_id)
            artist = list(artists)

            # retrieve youtube id
            new_artist_id = artist[0]['bilibili_id']

            pipeline = [
                {"$match": {
                    "user_id": new_artist_id,
                }},
                {"$sort": {"datetime": 1}},
                {"$match": {
                    "datetime": {
                        "$lte": date_end,
                        "$gt": start_date
                    }
                }},
                {"$unwind": "$data"},
                {"$group": {
                    "_id": "$datetime",
                    "user_id": {"$first": "$user_id"},
                    "count": {"$sum": {"$toInt": 1}},
                    "total_collect": {"$sum": "$data.collect"}
                }},
                {"$sort": {"_id": 1}},
                {"$project": {
                    "_id": 0,
                    "datetime": {
                        "$dateToString": {
                            "format": format,
                            "date": "$_id"
                    }},
                    "id": "$user_id",
                    "total_collect": "$total_collect",
                    "avg_collect": {
                        "$divide": [
                            "$total_collect", "$count"
                        ]
                    }
                }}
            ]

            results = Bilibili.objects().aggregate(pipeline)
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
    def get_engagement_rate(artist_id, date_end, range):
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
            # first get artist mid, then query spotify data
            # Check artist's MID, call method: get_artist_by_mid
            artists = BilibiliController.get_artist_by_mid(artist_id)
            artist = list(artists)

            # retrieve youtube id
            new_artist_id = artist[0]['bilibili_id']

            pipeline = [
                {"$match": {
                    "user_id": new_artist_id
                }},
                {"$sort": {"datetime": -1}},
                # match date range
                {"$match": {
                    "datetime": {
                        "$lte": date_end,
                        "$gt": start_date
                    }
                }},
                {"$unwind": "$data"},
                {"$group": {
                    "_id": "$datetime",
                    "user_id": {"$first": "$user_id"},
                    "count": {"$sum": {"$toInt": 1}},
                    "total_view": {"$sum": "$data.view"},
                    "total_like": {"$sum": "$data.like"},
                    "total_comment": {"$sum": "$data.comment"},
                    "total_share": {"$sum": "$data.share"},
                    "total_collect": {"$sum": "$data.collect"},
                    "total_coin": {"$sum": "$data.coin"},
                    "total_danmu": {"$sum": "$data.danmu"},
                }},
                {"$sort": {"_id": 1}},
                {"$project": {
                    "_id": 0,
                    "datetime": {
                        "$dateToString": {
                            "format": format,
                            "date": "$_id"
                    }},
                    "id": "$user_id",
                    "engagement_rate": {
                        "$divide": [{
                            "$sum": ["$total_like", "$total_comment", "$total_share", "$total_collect", "$total_coin",
                                     "$total_danmu"]
                        }, "$total_view"]
                    }
                }}
            ]

            results = Bilibili.objects().aggregate(pipeline)
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
    def get_latest_thirty_posts(artist_id):
        # Validate required parameters
        if not artist_id:
            return jsonify({'err': 'Missing artist_id parameter'}), 400

        try:
            # first get artist mid, then query spotify data
            # Check artist's MID, call method: get_artist_by_mid
            artists = BilibiliController.get_artist_by_mid(artist_id)
            artist = list(artists)
            # retrieve bilibili id
            new_artist_id = artist[0]['bilibili_id']

            pipeline = [
                {"$match": {
                    "user_id": new_artist_id
                }},
                {"$sort": {"datetime": -1}},
                {"$limit": 1},
                {"$project": {
                   "_id": 0,
                   "data": "$data"
                }},
                {"$unwind": "$data"},
                {"$project": {
                    "_id": 0,
                    "aid": "$data.aid",
                    "bvid": "$data.bvid",
                    "coin": "$data.coin",
                    "collect": "$data.collect",
                    "comment": "$data.comment",
                    "danmu": "$data.danmu",
                    "image": "$data.image",
                    "like": "$data.like",
                    "share": "$data.share",
                    "title": "$data.title",
                    "upload_date": "$data.upload_date",
                    "view": "$data.view"
                }}
            ]


            results = Bilibili.objects().aggregate(pipeline)
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
                "err": str(e)
            }), 500

    @staticmethod
    def get_bilibili_follower_growth(artist_id, campaign_start):
        if not artist_id or not campaign_start:
            return jsonify({
                "err": "Missing required parameters"
            }), 400

        try:
            campaign_start_dt = datetime.datetime.strptime(campaign_start, "%Y-%m-%d")
            result = BilibiliService.get_follower_growth(artist_id, campaign_start_dt)

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
    def get_bilibili_follower(artist_id, date_end, range):
       pass