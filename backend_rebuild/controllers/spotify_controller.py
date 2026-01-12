from models.spotify_model import Spotify
from models.artist_model import Artists
from models.user_model import Users
from services.spotify_service import SpotifyService
import datetime
from flask import request, jsonify, g
from libs.utils import get_current_user


class SpotifyController:
    @staticmethod
    # get spotify id by artist id
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
    # Get spotify follower
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
            # first get artist mid, then query spotify data
            # Check artist's MID, call method: get_artist_by_mid
            artists = SpotifyController.get_artist_by_mid(artist_id)
            artist = list(artists)
            # retrieve spotify id
            new_artist_id = artist[0]['spotify_id']

            pipeline = [
                # match artist spotify id
                {"$match": {
                    "spotify_id": str(new_artist_id)
                }},
                # sort by datetime
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
                    "id": "$spotify_id",
                    "follower": "$follower"
                }}
            ]

            results = Spotify.objects().aggregate(pipeline)

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
                'data': result,
            }), 200

        except Exception as e:
            return jsonify({
                'status': 'error',
                'err': str(e)
            }), 500

    @staticmethod
    # Get spotify monthly listener
    def get_monthly_listener(artist_id, date_end, range):
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
            # first get artist mid, then query spotify data
            # Check artist's MID, call method: get_artist_by_mid
            artists = SpotifyController.get_artist_by_mid(artist_id)
            artist = list(artists)
            # retrieve spotify id
            new_artist_id = artist[0]['spotify_id']

            pipeline = [
                # match artist spotify id
                {"$match": {
                    "spotify_id": str(new_artist_id)
                }},
                # sort by datetime
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
                    "id": "$spotify_id",
                    "monthly_listener": "$monthly_listener"
                }}
            ]

            results = Spotify.objects().aggregate(pipeline)

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
    # Get spotify popularity
    def get_popularity(artist_id, date_end, range):
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
            # first get artist mid, then query spotify data
            # Check artist's MID, call method: get_artist_by_mid
            artists = SpotifyController.get_artist_by_mid(artist_id)
            artist = list(artists)
            # retrieve spotify id
            new_artist_id = artist[0]['spotify_id']

            pipeline = [
                # match artist spotify id
                {"$match": {
                    "spotify_id": str(new_artist_id)
                }},
                # sort by datetime
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
                    "id": "$spotify_id",
                    "popularity": "$popularity"
                }}
            ]

            results = Spotify.objects().aggregate(pipeline)

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
    # Get spotify top 5 city
    def get_top_five_city(artist_id):
        # Validate required parameters
        if not artist_id:
            return jsonify({'err': 'Missing artist_id parameter'}), 400

        # first get artist mid, then query spotify data
        # Check artist's MID, call method: get_artist_by_mid
        artists = SpotifyController.get_artist_by_mid(artist_id)
        artist = list(artists)
        # retrieve spotify id
        new_artist_id = artist[0]['spotify_id']

        try:
            pipeline = [
                # match artist id
                {"$match": {
                    "spotify_id": new_artist_id
                }},
                # sort by date
                {"$sort": {"datetime": -1}},
                # limit latest record
                {"$limit": 1},
                # return fields
                {"$project": {
                    "_id": 0,
                    "datetime": {
                        "$dateToString": {
                            "format": "%Y-%m-%d",
                            "date": "$datetime"
                    }},
                    "id": "$spotify_id",
                    "top_city": "$top_country"
                }}
            ]

            results = Spotify.objects().aggregate(pipeline)

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
    # Get spotify fan conversion rate
    # Formula: (follower/monthly_listener)*100
    def get_conversion_rate(artist_id, date_end, range):
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
            # first get artist mid, then query spotify data
            # Check artist's MID, call method: get_artist_by_mid
            artists = SpotifyController.get_artist_by_mid(artist_id)
            artist = list(artists)
            # retrieve spotify id
            new_artist_id = artist[0]['spotify_id']

            pipeline = [
                    # match artist spotify id
                    {"$match": {
                        "spotify_id": str(new_artist_id)
                    }},
                    # sort by datetime
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
                        "id": "$spotify_id",
                        "date": {
                            "$dateToString": {
                                "format": "%Y-%m-%d",
                                "date": "$datetime"
                            }
                        },
                        "follower": "$follower",
                        "monthly_listener": "$monthly_listener"
                    }},
                    # add conversion rate field
                    {"$project": {
                        "_id": 0,
                        "datetime": "$date",
                        "conversion_rate": {
                            "$multiply": [{"$divide": ["$follower", "$monthly_listener"]}, 100]
                        }
                    }}
                ]

            results = Spotify.objects().aggregate(pipeline)

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
    # Get spotify top tracks by region
    def get_top_tracks_by_region(artist_id):
        # Validate required parameters
        if not artist_id:
            return jsonify({'err': 'Missing artist_id parameter'}), 400

        try:
            # first get artist mid, then query spotify data
            # Check artist's MID, call method: get_artist_by_mid
            artists = SpotifyController.get_artist_by_mid(artist_id)
            artist = list(artists)
            # retrieve spotify id
            new_artist_id = artist[0]['spotify_id']

            # get track title
            get_track_title_pipeline = [
                {"$match": {
                    "spotify_id": new_artist_id
                }},
                {"$sort": {"datetime": -1}},
                {"$limit": 1},
                {"$project": {
                    "_id": 0,
                    "datetime": {
                        "$dateToString": {
                            "format": "%Y-%m-%d",
                            "date": "$datetime"
                        }
                    },
                    "top_track": "$top_track"
                }},
                {"$unwind": "$top_track"},
                {"$project": {
                    "_id": 0,
                    "datetime": "$datetime",
                    "region": "$top_track.region",
                    "country": "$top_track.country",
                    "tracks": "$top_track.tracks"
                }},
                {"$unwind": "$tracks"},
                {"$group": {
                    "_id": "$tracks.track",
                    "count": {"$sum": {"$toInt": 1}},
                    "popularity": {"$sum": "$tracks.popularity"}
                }},
                {"$project": {
                    "_id": 0,
                    "tracks": "$_id"
                }},
                {"$group": {
                    "_id": None,
                    "tracks": {"$push": "$tracks"}
                }},
                {"$project": {
                    "_id": 0
                }}
            ]

            # get track query
            pipeline = [
                {"$match": {
                    "spotify_id": new_artist_id
                }},
                {"$sort": {"datetime": -1}},
                {"$limit": 1},
                {"$unwind": "$top_track"},
                {"$project": {
                    "_id": 0,
                    "datetime": {
                        "$dateToString": {
                            "format": "%Y-%m-%d",
                            "date": "$datetime"
                        }
                    },
                    "region": "$top_track.region",
                    "country": "$top_track.country",
                    "tracks": "$top_track.tracks"
                }},
                {"$unwind": "$tracks"},
                {"$sort": {"tracks.popularity": -1}},
                {"$group": {
                    "_id": {"region": "$region", "track": "$tracks.track"},
                    "count": {"$sum": {"$toInt": 1}},
                    "popularity": {"$sum": "$tracks.popularity"}
                }},
                {"$addFields": {
                    "agg_popularity": {
                        "$toInt": {
                            "$round": [{"$divide": ["$popularity", "$count"]}, 2]}
                    }
                }},
                {"$group": {
                    "_id": "$_id.track",
                    "region": {"$push": "$_id.region"},
                    "agg_popularity": {"$push": "$agg_popularity"}
                }},
                {"$project": {
                    "track_info": {
                        "$map": {
                            "input": {"$zip": {"inputs": ["$region", "$agg_popularity"]}},
                            "in": {
                                "region": {"$arrayElemAt": ["$$this", 0]},
                                "agg_popularity": {"$arrayElemAt": ["$$this", 1]}
                            }
                        }
                    }
                }}
            ]

            track_lists = Spotify.objects().aggregate(get_track_title_pipeline)
            track_lists_result = list(track_lists)
            results = Spotify.objects().aggregate(pipeline)
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
                'data': result,
                'track_list_result': track_lists_result
            }), 200

        except Exception as e:
            return jsonify({
                'status': 'error',
                'err': str(e)
            })

    @staticmethod
    # Get spotify top tracks by country
    def get_top_tracks_by_country(artist_id, country):
        # Validate required parameters
        if not artist_id:
            return jsonify({'err': 'Missing artist_id parameter'}), 400

        try:
            # first get artist mid, then query spotify data
            # Check artist's MID, call method: get_artist_by_mid
            artists = SpotifyController.get_artist_by_mid(artist_id)
            artist = list(artists)
            # retrieve spotify id
            new_artist_id = artist[0]['spotify_id']

            pipeline = [
                {"$match": {
                    "spotify_id": new_artist_id
                }},
                {"$sort": {"datetime": -1}},
                {"$limit": 1},
                {"$unwind": "$top_track"},
                # match country
                {"$match": {
                    "top_track.country": country
                }},
                {"$project": {
                    "_id": 0,
                    "datetime": {
                        "$dateToString": {
                            "format": "%Y-%m-%d",
                            "date": "$datetime"
                        }
                    },
                    "country": "$top_track.country",
                    "top_track": "$top_track.tracks",
                }},
                {"$unwind": "$top_track"},
                {"$sort": {"top_track.popularity": -1}},
                {"$group": {
                    "_id": {"datetime": "$datetime", country: "$country"},
                    "top_track": { "$push": "$top_track"}
                }},
                {"$project": {
                    "_id": 0,
                    "datetime": "$_id.datetime",
                    "country": "$_id.country",
                    "top_track": "$top_track"
                }}
            ]

            results = Spotify.objects().aggregate(pipeline)
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
            }), 500

    @staticmethod
    def get_spotify_follower_growth(artist_id, campaign_start):
        if not artist_id or not campaign_start:
            return jsonify({
                "err": "Missing required parameters"
            }), 400

        try:
            campaign_start_dt = datetime.datetime.strptime(campaign_start, "%Y-%m-%d")
            result = SpotifyService.get_follower_growth(artist_id, campaign_start_dt)

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
    def get_spotify_popularity_growth(artist_id, campaign_start):
        if not artist_id or not campaign_start:
            return jsonify({
                "err": "Missing required parameters"
            }), 400

        try:
            campaign_start_dt = datetime.datetime.strptime(campaign_start, "%Y-%m-%d")
            result = SpotifyService.get_popularity_growth(artist_id, campaign_start_dt)

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
    def get_spotify_monthly_listener_growth(artist_id, campaign_start):
        if not artist_id or not campaign_start:
            return jsonify({
                "err": "Missing required parameters"
            }), 400

        try:
            campaign_start_dt = datetime.datetime.strptime(campaign_start, "%Y-%m-%d")
            result = SpotifyService.get_monthly_listener_growth(artist_id, campaign_start_dt)

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
    def get_spotify_top_five_city_growth(artist_id, campaign_start):
        if not artist_id or not campaign_start:
            return jsonify({
                "err": "Missing required parameters"
            }), 400

        try:
            campaign_start_dt = datetime.datetime.strptime(campaign_start, "%Y-%m-%d")
            result = SpotifyService.get_top_five_city_growth(artist_id, campaign_start_dt)

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
    def get_spotify_follower(artist_id, date_end, range):
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
            result = SpotifyService.get_chart_follower(
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
    def get_spotify_monthly_listener(artist_id, date_end, range):
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
            result = SpotifyService.get_chart_monthly_listener(
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

    ########### v2 endpoint ###########
    def get_spotify_follower_by_artist_id(artist_id):
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

        # query spotify data
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
            spotify_data = Spotify.objects(
                spotify_id=matched_artist.spotify_id,
                datetime__gte=start_date,
                datetime__lte=date_end
            ).order_by("datetime")

            if not spotify_data:
                return jsonify({
                    "error": "No spotify data found"
                }), 404

            result = []
            for s in spotify_data:
                result.append({
                    "datetime": s.datetime.strftime("%Y-%m-%d"),
                    "spotify_id": s.spotify_id,
                    "follower": s.follower,
                })

            return jsonify({
                "status": "success",
                "data": result
            }), 200
        except Exception as e:
            return jsonify({
                "error": str(e)
            }), 500

    def get_spotify_monthly_listener_by_artist_id(artist_id):
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

        # query spotify data
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
            spotify_data = Spotify.objects(
                spotify_id=matched_artist.spotify_id,
                datetime__gte=start_date,
                datetime__lte=date_end
            ).order_by("datetime")

            if not spotify_data:
                return jsonify({
                    "error": "No spotify data found"
                }), 404

            result = []
            for s in spotify_data:
                result.append({
                    "datetime": s.datetime.strftime("%Y-%m-%d"),
                    "spotify_id": s.spotify_id,
                    "monthly_listener": s.monthly_listener,
                })

            return jsonify({
                "status": "success",
                "data": result
            }), 200
        except Exception as e:
            return jsonify({
                "error": str(e)
            }), 500

    def get_spotify_popularity_by_artist_id(artist_id):
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

        # query spotify data
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
            spotify_data = Spotify.objects(
                spotify_id=matched_artist.spotify_id,
                datetime__gte=start_date,
                datetime__lte=date_end
            ).order_by("datetime")

            if not spotify_data:
                return jsonify({
                    "error": "No spotify data found"
                }), 404

            result = []
            for s in spotify_data:
                result.append({
                    "datetime": s.datetime.strftime("%Y-%m-%d"),
                    "spotify_id": s.spotify_id,
                    "popularity": s.popularity,
                })

            return jsonify({
                "status": "success",
                "data": result
            }), 200
        except Exception as e:
            return jsonify({
                "error": str(e)
            }), 500

    def get_spotify_top_five_city_by_artist_id(artist_id):
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
            spotify_data = Spotify.objects(
                spotify_id=matched_artist.spotify_id,
            ).order_by("-datetime").limit(1)

            if not spotify_data:
                return jsonify({
                    "error": "No spotify data found"
                }), 404

            result = []
            for s in spotify_data:
                result.append({
                    "datetime": s.datetime.strftime("%Y-%m-%d"),
                    "spotify_id": s.spotify_id,
                    "top_city": [
                        {
                            "country": tc.country,
                            "city": tc.city,
                            "listener": tc.listener
                        } for tc in s.top_country
                    ] if s.top_country else [],
                })

            return jsonify({
                "status": "success",
                "data": result
            }), 200

        except Exception as e:
            return jsonify({
                "error": str(e)
            }), 500

    def get_spotify_conversion_rate_by_artist_id(artist_id):
        """
        Get spotify fan conversion rate
        Formula: (follower/monthly_listener)*100
        :return:
        """
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

        # query spotify data
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
                # match artist spotify id
                {"$match": {
                    "spotify_id": matched_artist.spotify_id
                }},
                # sort by datetime
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
                    "id": "$spotify_id",
                    "date": {
                        "$dateToString": {
                            "format": "%Y-%m-%d",
                            "date": "$datetime"
                        }
                    },
                    "follower": "$follower",
                    "monthly_listener": "$monthly_listener"
                }},
                # add conversion rate field
                {"$project": {
                    "_id": 0,
                    "datetime": "$date",
                    "conversion_rate": {
                        "$multiply": [{"$divide": ["$follower", "$monthly_listener"]}, 100]
                    }
                }}
            ]
            spotify_data = Spotify.objects().aggregate(pipeline)

            if not spotify_data:
                return jsonify({
                    "error": "No spotify data found"
                }), 404

            result = list(spotify_data)

            return jsonify({
                "status": "success",
                "data": result
            }), 200
        except Exception as e:
            return jsonify({
                "error": str(e)
            }), 500

    def get_spotify_top_tracks_by_country_by_artist_id(artist_id):
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

        country = request.args.get("country")
        if not country:
            return jsonify({
                "error": "Missing country"
            }), 400

        try:
            pipeline = [
                {"$match": {
                    "spotify_id": matched_artist.spotify_id
                }},
                {"$sort": {"datetime": -1}},
                {"$limit": 1},
                {"$unwind": "$top_track"},
                # match country
                {"$match": {
                    "top_track.country": country
                }},
                {"$project": {
                    "_id": 0,
                    "datetime": {
                        "$dateToString": {
                            "format": "%Y-%m-%d",
                            "date": "$datetime"
                        }
                    },
                    "spotify_id": "$spotify_id",
                    "country": "$top_track.country",
                    "top_track": "$top_track.tracks",
                }},
                {"$unwind": "$top_track"},
                {"$sort": {"top_track.popularity": -1}},
                {"$group": {
                    "_id": {"datetime": "$datetime", "country": "$country"},
                    "spotify_id": {"$first": "$spotify_id"},
                    "top_track": {"$push": "$top_track"}
                }},
                {"$project": {
                    "_id": 0,
                    "datetime": "$_id.datetime",
                    "spotify_id": "$spotify_id",
                    "country": "$_id.country",
                    "top_track": "$top_track"
                }}
            ]

            spotify_data = Spotify.objects().aggregate(pipeline)
            if not spotify_data:
                return jsonify({
                    "error": "No spotify data found"
                }), 404

            result = list(spotify_data)

            return jsonify({
                "status": "success",
                "data": result
            }), 200

        except Exception as e:
            return jsonify({
                "error": str(e)
            }), 500

    def get_spotify_top_tracks_by_region(artist_id):
        pass
