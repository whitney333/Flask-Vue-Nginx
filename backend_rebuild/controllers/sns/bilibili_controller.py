from models.sns.bilibili_model import Bilibili
from models.artist_model import Artists
import datetime
from flask import jsonify, request
from services.bilibili_service import BilibiliService
from libs.utils import get_current_user


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
            result = BilibiliService.get_chart_follower(
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
    def get_bilibili_views(artist_id, date_end, range):
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
            result = BilibiliService.get_chart_view(
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
    def get_bilibili_likes(artist_id, date_end, range):
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
            result = BilibiliService.get_chart_like(
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
    def get_bilibili_comments(artist_id, date_end, range):
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
            result = BilibiliService.get_chart_comment(
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
    def get_bilibili_shares(artist_id, date_end, range):
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
            result = BilibiliService.get_chart_share(
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
    def get_bilibili_danmus(artist_id, date_end, range):
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
            result = BilibiliService.get_chart_danmu(
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
    def get_bilibili_coins(artist_id, date_end, range):
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
            result = BilibiliService.get_chart_coin(
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
    def get_bilibili_collects(artist_id, date_end, range):
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
            result = BilibiliService.get_chart_collect(
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
    def get_bilibili_engagement(artist_id, date_end, range):
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
            result = BilibiliService.get_chart_engagement_rate(
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
    def get_bilibili_latest_videos(artist_id):
        # get user info
        user = get_current_user(optional=True)

        try:
            data = BilibiliService.get_posts(
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
