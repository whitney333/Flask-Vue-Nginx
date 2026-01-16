from models.sns.tiktok_model import Tiktok, TiktokVideo
from models.artist_model import Artists
import datetime
from flask import jsonify, request
from services.tiktok_service import TiktokService
from libs.utils import get_current_user


class TiktokController:
    @staticmethod
    def get_tiktok_video_index(self):
        ## TODO FIX SCRAPING POSTS METHOD
        pass

    @staticmethod
    def get_tiktok_follower_growth(artist_id, campaign_start):
        if not artist_id or not campaign_start:
            return jsonify({
                "err": "Missing required parameters"
            }), 400

        try:
            campaign_start_dt = datetime.datetime.strptime(campaign_start, "%Y-%m-%d")
            result = TiktokService.get_follower_growth(artist_id, campaign_start_dt)

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
    def get_tiktok_hashtag_growth(artist_id, campaign_start):
        if not artist_id or not campaign_start:
            return jsonify({
                "err": "Missing required parameters"
            }), 400

        try:
            campaign_start_dt = datetime.datetime.strptime(campaign_start, "%Y-%m-%d")
            result = TiktokService.get_hashtag_growth(artist_id, campaign_start_dt)

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
    def get_tiktok_follower(artist_id, date_end, range):
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
            result = TiktokService.get_chart_follower(
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
    def get_tiktok_likes(artist_id, date_end, range):
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
            result = TiktokService.get_chart_like(
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
    def get_tiktok_hashtags(artist_id, date_end, range):
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
            result = TiktokService.get_chart_hashtag(
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
    def get_tiktok_most_used_hashtag(artist_id, date_end, range):
        pass

    @staticmethod
    def get_tiktok_most_engaged_hashtag(artist_id, date_end, range):
        pass
