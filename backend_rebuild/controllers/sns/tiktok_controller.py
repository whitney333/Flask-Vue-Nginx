from models.sns.tiktok_model import Tiktok, TiktokVideo
import datetime
from flask import jsonify, request

class TiktokController:
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
        Get TikTok follower count data for a specific time range
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
                        {"id": artist_id},
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
                    "follower": "$follower"
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
        """
        Get TikTok hashtag data for a specific time range
        :param artist_id: The ID of the artist to get hashtag data for
        :param date_end: The end date for the data range in format 'YYYY-MM-DD'
        :param range: The time range to analyze ('7d', '28d', '90d', '180d', '365d')
        :return: JSON response containing hashtag data with dates and counts
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
                        {"id": artist_id},
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
                    "hashtag": "$hashtag"
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
    def get_like(artist_id, date_end, range):
        """
        Get TikTok like count data for a specific time range
        :param artist_id: The ID of the artist to get like data for
        :param date_end: The end date for the data range in format 'YYYY-MM-DD'
        :param range: The time range to analyze ('7d', '28d', '90d', '180d', '365d')
        :return: JSON response containing like data with dates and counts
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
                        {"id": artist_id},
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
                    "like": "$like"
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

    def get_tiktok_video_index(self):
        pass
