from models.melon_model import Melon
from models.artist_model import Artists
from models.user_model import Users
from flask import jsonify, request
import datetime
from libs.utils import get_current_user
from services.melon_service import MelonService


class MelonController:
    @staticmethod
    # get melon id by artist id
    def get_artist_by_mid(artist_id):
        # Validate required parameters
        if not artist_id:
            return jsonify({'err': 'Missing artist_id parameter'}), 400
        try:
            pipeline = [
                {"$match": {
                    # match artist id
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

            # mongodb pipeline
            # first get artist mid, then query melon data
            # Check artist's MID, call method: get_artist_by_mid
            artists = MelonController.get_artist_by_mid(artist_id)
            artist = list(artists)
            # retrieve melon id
            new_artist_id = artist[0]['melon_id']

            pipeline = [
                # match artist id in string format
                {"$match": {
                    "melon_id": str(new_artist_id)
                }},
                # sort by date
                {"$sort": {"datetime": 1}},
                # match date range
                {"$match": {
                    "datetime": {
                        "$lte": date_end,
                        "$gt": start_date
                    }
                }},
                # projection
                {"$project": {
                    "_id": 0,
                    "datetime": {
                        "$dateToString": {
                            "format": "%Y-%m-%d",
                            "date": "$datetime"
                        }
                    },
                    "melon_id": "$melon_id",
                    "follower": "$follower"
                }}
            ]

            results = Melon.objects().aggregate(pipeline)

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

    def get_melon_follower_by_artist_id(artist_id):
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
            melon_data = Melon.objects(
                melon_id=matched_artist.melon_id,
                datetime__gte=start_date,
                datetime__lte=date_end
            ).order_by("datetime")

            if not melon_data:
                return jsonify({
                    "error": "No melon data found"
                }), 404

            result = []
            for m in melon_data:
                result.append({
                    "datetime": m.datetime,
                    "melon_id": m.melon_id,
                    "follower": m.follower,
                })
            return jsonify({
                "status": "success",
                "data": result
            }), 200
        except Exception as e:
            return jsonify({
                "error": str(e)
            }), 500

    @staticmethod
    def get_melon_follower(artist_id, date_end, range):
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
            result = MelonService.get_chart_follower(
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
                    "is_premium": result["meta"]["is_premium"]
                }
            }), 200

        return jsonify({
            "status": "success",
            "data": result["data"],
            "meta": result["meta"]
        }), 200
