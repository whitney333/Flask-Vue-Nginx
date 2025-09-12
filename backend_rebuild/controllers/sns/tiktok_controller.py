from models.sns.tiktok_model import Tiktok, TiktokVideo
from models.artist_model import Artists
import datetime
from flask import jsonify, request

class TiktokController:
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

    # TODO Tiktok scraping method fix
    # get most-used hashtags
    def get_hashtags_most_used_recent_ten(self):
        pass

    # get most-engaged hashtags
    def get_hashtags_most_engaged_recent_ten(self):
        pass

    @staticmethod
    def get_follower(artist_id, date_end, range):
        """
        Get Tiktok follower data for a specific time range
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
            # first get artist mid, then query spotify data
            # Check artist's MID, call method: get_artist_by_mid
            artists = TiktokController.get_artist_by_mid(artist_id)
            artist = list(artists)
            # retrieve id
            new_artist_id = artist[0]['tiktok_id']

            pipeline = [
                # match artist id
                {"$match": {
                    "id": new_artist_id
                }},
                {"$sort": {"datetime": 1}},
                # match date range
                {"$match": {
                    "datetime": {
                        "$lte": date_end,
                        "$gt": start_date
                    }
                }},
                # return fields
                {"$project": {
                    "_id": 0,
                    "datetime": {
                        "$dateToString": {
                            "format": "%Y-%m-%d",
                            "date": "$datetime"
                        }
                    },
                    "follower": {"$toInt": "$follower"}
                }}
            ]

            # Execute pipeline
            results = Tiktok.objects().aggregate(pipeline)

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
    def get_hashtag(artist_id, date_end, range):
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
            artists = TiktokController.get_artist_by_mid(artist_id)
            artist = list(artists)
            # retrieve id
            new_artist_id = artist[0]['tiktok_id']

            pipeline = [
                # match artist id
                {"$match": {
                    "id": new_artist_id
                }},
                {"$sort": {"datetime": 1}},
                # match date range
                {"$match": {
                    "datetime": {
                        "$lte": date_end,
                        "$gt": start_date
                    }
                }},
                # return fields
                {"$project": {
                    "_id": 0,
                    "datetime": {
                        "$dateToString": {
                            "format": "%Y-%m-%d",
                            "date": "$datetime"
                        }
                    },
                    "hashtag": {"$toInt": "$hashtag"}
                }}
            ]

            results = Tiktok.objects().aggregate(pipeline)

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
                'err': str(e)
            }), 500

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
            artists = TiktokController.get_artist_by_mid(artist_id)
            artist = list(artists)
            # retrieve id
            new_artist_id = artist[0]['tiktok_id']

            pipeline = [
                # match artist id
                {"$match": {
                    "id": new_artist_id
                }},
                {"$sort": {"datetime": 1}},
                # match date range
                {"$match": {
                    "datetime": {
                        "$lte": date_end,
                        "$gt": start_date
                    }
                }},
                # return fields
                {"$project": {
                    "_id": 0,
                    "datetime": {
                        "$dateToString": {
                            "format": "%Y-%m-%d",
                            "date": "$datetime"
                        }
                    },
                    "like": {"$toInt": "$like"}
                }}
            ]

            results = Tiktok.objects().aggregate(pipeline)

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
                'err': str(e)
            }), 500

    def get_tiktok_video_index(self):
        ## TODO FIX SCRAPING POSTS METHOD
        pass
