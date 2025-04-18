from models.spotify_model import Spotify
import datetime
from flask import request, jsonify

class SpotifyController:
    @staticmethod
    # Get spotify follower
    def get_follower(artist_id, date_end, range):
        if not all([artist_id, date_end, range]):
            return jsonify({'err': 'Missing required parameters'}), 400

        try:
            format = "%Y-%m-%d"
            date_end = datetime.datetime.strptime(date_end, format)

            # Case 1
            if (range == "7d"):
                # calculate the date 7 days ago from today
                seven_days_ago = date_end - datetime.timedelta(days=7)

                pipeline = [
                # match artist spotify id
                {"$match": {
                    "spotify_id": str(artist_id)
                }},
                # sort by datetime
                {"$sort": {"datetime": 1}},
                # match date range
                {"$match": {
                    "datetime": {
                        "$lte": date_end,
                        "$gt": seven_days_ago
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

                result = []
                for item in results:
                    result.append(item)
                # print(result)

                return jsonify({
                    'status': 'success',
                    'data': result
                }), 200
            # Case 2
            elif (range == "28d"):
                # calculate the date 28 days ago from today
                twenty_eight_days_ago = datetime.datetime.now() - datetime.timedelta(days=28)

                pipeline = [
                # match artist spotify id
                {"$match": {
                    "spotify_id": str(artist_id)
                }},
                # sort by datetime
                {"$sort": {"datetime": 1}},
                # match date range
                {"$match": {
                    "datetime": {
                        "$lte": date_end,
                        "$gt": twenty_eight_days_ago
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

                result = []
                for item in results:
                    result.append(item)
                # print(result)

                return jsonify({
                    'status': 'success',
                    'data': result
                }), 200
            # Case 3
            elif (range == "90d"):
                # calculate the date 90 days ago from today
                ninety_days_ago = datetime.datetime.now() - datetime.timedelta(days=90)

                pipeline = [
                # match artist spotify id
                {"$match": {
                    "spotify_id": str(artist_id)
                }},
                # sort by datetime
                {"$sort": {"datetime": 1}},
                # match date range
                {"$match": {
                    "datetime": {
                        "$lte": date_end,
                        "$gt": ninety_days_ago
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

                result = []
                for item in results:
                    result.append(item)
                # print(result)

                return jsonify({
                    'status': 'success',
                    'data': result
                }), 200
            # Case 4: return 180 days followers data
            elif (range == "180d"):
                # calculate the date 180 days ago from today
                hundred_eighty_days_ago = datetime.datetime.now() - datetime.timedelta(days=180)

                pipeline = [
                # match artist spotify id
                {"$match": {
                    "spotify_id": str(artist_id)
                }},
                # sort by datetime
                {"$sort": {"datetime": 1}},
                # match date range
                {"$match": {
                    "datetime": {
                        "$lte": date_end,
                        "$gt": hundred_eighty_days_ago
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

                result = []
                for item in results:
                    result.append(item)
                # print(result)

                return jsonify({
                    'status': 'success',
                    'data': result
                }), 200
            # Case 5: return a year followers data
            elif (range == "365d"):
                # calculate the date 180 days ago from today
                year_ago = datetime.datetime.now() - datetime.timedelta(days=365)

                pipeline = [
                # match artist spotify id
                {"$match": {
                    "spotify_id": str(artist_id)
                }},
                # sort by datetime
                {"$sort": {"datetime": 1}},
                # match date range
                {"$match": {
                    "datetime": {
                        "$lte": date_end,
                        "$gt": year_ago
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

                result = []
                for item in results:
                    result.append(item)
                # print(result)

                return jsonify({
                    'status': 'success',
                    'data': result
                }), 200
            # return 7 days followers data
            else:
                # calculate the date 7 days ago from today
                seven_days_ago = date_end - datetime.timedelta(days=7)

                pipeline = [
                # match artist spotify id
                {"$match": {
                    "spotify_id": str(artist_id)
                }},
                # sort by datetime
                {"$sort": {"datetime": 1}},
                # match date range
                {"$match": {
                    "datetime": {
                        "$lte": date_end,
                        "$gt": seven_days_ago
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

                result = []
                for item in results:
                    result.append(item)
                #   print(result)

                return jsonify({
                    'status': 'success',
                    'data': result
                }), 200
        except Exception as e:
            return jsonify({
                'err': str(e)
            }), 500

    @staticmethod
    # Get spotify monthly listener
    def get_monthly_listener(artist_id, date_end, range):
        if not all([artist_id, date_end, range]):
            return jsonify({'err': 'Missing required parameters'}), 400

        try:
            format = "%Y-%m-%d"
            date_end = datetime.datetime.strptime(date_end, format)

            # Case 1
            if (range == "7d"):
                # calculate the date 7 days ago from today
                seven_days_ago = date_end - datetime.timedelta(days=7)
                pipeline = [
            # match artist spotify id
            {"$match": {
                "spotify_id": str(artist_id)
            }},
            # sort by datetime
            {"$sort": {"datetime": 1}},
            # match date range
            {"$match": {
                "datetime": {
                    "$lte": date_end,
                    "$gt": seven_days_ago
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

                result = []
                for item in results:
                    result.append(item)
                # print(result)

                return jsonify({
                    'status': 'success',
                    'data': result
                }), 200
            elif (range == "28d"):
                twenty_eight_days_ago = datetime.datetime.now() - datetime.timedelta(days=28)

                pipeline = [
                # match artist spotify id
                {"$match": {
                    "spotify_id": str(artist_id)
                }},
                # sort by datetime
                {"$sort": {"datetime": 1}},
                # match date range
                {"$match": {
                    "datetime": {
                        "$lte": date_end,
                        "$gt": twenty_eight_days_ago
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

                result = []
                for item in results:
                    result.append(item)
                # print(result)

                return jsonify({
                    'status': 'success',
                    'data': result
                }), 200
            elif (range == "90d"):
                ninety_days_ago = datetime.datetime.now() - datetime.timedelta(days=90)

                pipeline = [
                # match artist spotify id
                {"$match": {
                    "spotify_id": str(artist_id)
                }},
                # sort by datetime
                {"$sort": {"datetime": 1}},
                # match date range
                {"$match": {
                    "datetime": {
                        "$lte": date_end,
                        "$gt": ninety_days_ago
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

                result = []
                for item in results:
                    result.append(item)
                # print(result)

                return jsonify({
                    'status': 'success',
                    'data': result
                }), 200
            elif (range == "180d"):
                hundred_eighty_days_ago = datetime.datetime.now() - datetime.timedelta(days=180)

                pipeline = [
                # match artist spotify id
                {"$match": {
                    "spotify_id": str(artist_id)
                }},
                # sort by datetime
                {"$sort": {"datetime": 1}},
                # match date range
                {"$match": {
                    "datetime": {
                        "$lte": date_end,
                        "$gt": hundred_eighty_days_ago
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

                result = []
                for item in results:
                    result.append(item)
                # print(result)

                return jsonify({
                    'status': 'success',
                    'data': result
                }), 200
            elif (range == "365d"):
                year_ago = datetime.datetime.now() - datetime.timedelta(days=365)

                pipeline = [
                # match artist spotify id
                {"$match": {
                    "spotify_id": str(artist_id)
                }},
                # sort by datetime
                {"$sort": {"datetime": 1}},
                # match date range
                {"$match": {
                    "datetime": {
                        "$lte": date_end,
                        "$gt": year_ago
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

                result = []
                for item in results:
                    result.append(item)
                # print(result)

                return jsonify({
                    'status': 'success',
                    'data': result
                }), 200
            else:
                # calculate the date 7 days ago from today
                seven_days_ago = date_end - datetime.timedelta(days=7)
                pipeline = [
                # match artist spotify id
                {"$match": {
                    "spotify_id": str(artist_id)
                }},
                # sort by datetime
                {"$sort": {"datetime": 1}},
                # match date range
                {"$match": {
                    "datetime": {
                        "$lte": date_end,
                        "$gt": seven_days_ago
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

                result = []
                for item in results:
                    result.append(item)
                # print(result)

                return jsonify({
                    'status': 'success',
                    'data': result
                }), 200
        except Exception as e:
            return jsonify({
                'err': str(e)
            }), 500


    @staticmethod
    # Get spotify popularity
    def get_popularity(artist_id, date_end, range):
        if not all([artist_id, date_end, range]):
            return jsonify({'err': 'Missing required parameters'}), 400

        try:
            format = "%Y-%m-%d"
            date_end = datetime.datetime.strptime(date_end, format)

            # Case 1
            if (range == "7d"):
                # calculate the date 7 days ago from today
                seven_days_ago = date_end - datetime.timedelta(days=7)

                pipeline = [
                # match artist spotify id
                {"$match": {
                    "spotify_id": str(artist_id)
                }},
                # sort by datetime
                {"$sort": {"datetime": 1}},
                # match date range
                {"$match": {
                    "datetime": {
                        "$lte": date_end,
                        "$gt": seven_days_ago
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

                result = []
                for item in results:
                    result.append(item)
                # print(result)

                return jsonify({
                    'status': 'success',
                    'data': result
                }), 200
            elif (range == "28d"):
                twenty_eight_days_ago = datetime.datetime.now() - datetime.timedelta(days=28)

                pipeline = [
                # match artist spotify id
                {"$match": {
                    "spotify_id": str(artist_id)
                }},
                # sort by datetime
                {"$sort": {"datetime": 1}},
                # match date range
                {"$match": {
                    "datetime": {
                        "$lte": date_end,
                        "$gt": twenty_eight_days_ago
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

                result = []
                for item in results:
                    result.append(item)
                # print(result)

                return jsonify({
                    'status': 'success',
                    'data': result
                }), 200
            elif (range == "90d"):
                ninety_days_ago = datetime.datetime.now() - datetime.timedelta(days=90)

                pipeline = [
                # match artist spotify id
                {"$match": {
                    "spotify_id": str(artist_id)
                }},
                # sort by datetime
                {"$sort": {"datetime": 1}},
                # match date range
                {"$match": {
                    "datetime": {
                        "$lte": date_end,
                        "$gt": ninety_days_ago
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

                result = []
                for item in results:
                    result.append(item)
                # print(result)

                return jsonify({
                    'status': 'success',
                    'data': result
                }), 200
            elif (range == "180d"):
                hundred_eighty_days_ago = datetime.datetime.now() - datetime.timedelta(days=180)

                pipeline = [
                # match artist spotify id
                {"$match": {
                    "spotify_id": str(artist_id)
                }},
                # sort by datetime
                {"$sort": {"datetime": 1}},
                # match date range
                {"$match": {
                    "datetime": {
                        "$lte": date_end,
                        "$gt": hundred_eighty_days_ago
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

                result = []
                for item in results:
                    result.append(item)
                # print(result)

                return jsonify({
                    'status': 'success',
                    'data': result
                }), 200
            elif (range == "365d"):
                year_ago = datetime.datetime.now() - datetime.timedelta(days=365)

                pipeline = [
                # match artist spotify id
                {"$match": {
                    "spotify_id": str(artist_id)
                }},
                # sort by datetime
                {"$sort": {"datetime": 1}},
                # match date range
                {"$match": {
                    "datetime": {
                        "$lte": date_end,
                        "$gt": year_ago
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

                result = []
                for item in results:
                    result.append(item)
                # print(result)

                return jsonify({
                    'status': 'success',
                    'data': result
                }), 200
            else:
                # calculate the date 7 days ago from today
                seven_days_ago = date_end - datetime.timedelta(days=7)

                pipeline = [
                # match artist spotify id
                {"$match": {
                    "spotify_id": str(artist_id)
                }},
                # sort by datetime
                {"$sort": {"datetime": 1}},
                # match date range
                {"$match": {
                    "datetime": {
                        "$lte": date_end,
                        "$gt": seven_days_ago
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

                result = []
                for item in results:
                    result.append(item)
                # print(result)

                return jsonify({
                    'status': 'success',
                    'data': result
                }), 200
        except Exception as e:
            return jsonify({
                'err': str(e)
            }), 500

    # Get spotify top 5 city
    def get_top_five_city(artist_id):
        pipeline = [
            # match artist id
            {"$match": {
                "spotify_id": "0jxjOumN4dyPFTLUojSbNP"
            }},
            # sort by date
            {"$sort": {"datetime": -1}},
            # limit latest record
            {"$limit": 1},
            # return fields
            {"$project": {
                "_id": 0,
                "id": "$spotify_id",
                "top_city": "$top_country"
            }}
        ]

        results = Spotify.objects().aggregate(pipeline)

        result = []
        for item in results:
            result.append(item)
        # print(result)

        return result

    @staticmethod
    # Get spotify fan conversion rate
    # Formula: (follower/monthly_listener)*100
    def get_conversion_rate(artist_id, date_end, range):
        if not all([artist_id, date_end, range]):
            return jsonify({'err': 'Missing required parameters'}), 400

        try:
            if (range == "7d"):
                # calculate the date 7 days ago from today
                seven_days_ago = date_end - datetime.timedelta(days=7)

                pipeline = [
                # match artist spotify id
                {"$match": {
                    "spotify_id": str(artist_id)
                }},
                # sort by datetime
                {"$sort": {"datetime": 1}},
                # match date range
                {"$match": {
                    "datetime": {
                        "$lte": date_end,
                        "$gt": seven_days_ago
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
                        "$round": [{"$multiply": [{"$divide": ["$follower", "$monthly_listener"]}, 100]}, 2]
                    }
                }}
            ]

                results = Spotify.objects().aggregate(pipeline)

                result = []
                for item in results:
                    result.append(item)
                # print(result)

                return jsonify({
                    'status': 'success',
                    'data': result
                }), 200
            elif (range == "28d"):
                twenty_eight_days_ago = datetime.datetime.now() - datetime.timedelta(days=28)

                pipeline = [
                # match artist spotify id
                {"$match": {
                    "spotify_id": str(artist_id)
                }},
                # sort by datetime
                {"$sort": {"datetime": 1}},
                # match date range
                {"$match": {
                    "datetime": {
                        "$lte": date_end,
                        "$gt": twenty_eight_days_ago
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
                        "$round": [{"$multiply": [{"$divide": ["$follower", "$monthly_listener"]}, 100]}, 2]
                    }
                }}
            ]

                results = Spotify.objects().aggregate(pipeline)

                result = []
                for item in results:
                    result.append(item)
                # print(result)

                return jsonify({
                    'status': 'success',
                    'data': result
                }), 200
            elif (range == "90d"):
                # calculate the date 90 days ago from today
                ninety_days_ago = date_end - datetime.timedelta(days=7)

                pipeline = [
                # match artist spotify id
                {"$match": {
                    "spotify_id": str(artist_id)
                }},
                # sort by datetime
                {"$sort": {"datetime": 1}},
                # match date range
                {"$match": {
                    "datetime": {
                        "$lte": date_end,
                        "$gt": ninety_days_ago
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
                        "$round": [{"$multiply": [{"$divide": ["$follower", "$monthly_listener"]}, 100]}, 2]
                    }
                }}
            ]

                results = Spotify.objects().aggregate(pipeline)

                result = []
                for item in results:
                    result.append(item)
                # print(result)

                return jsonify({
                    'status': 'success',
                    'data': result
                }), 200
            elif (range == "180d"):
                hundred_eighty_days_ago = datetime.datetime.now() - datetime.timedelta(days=180)
                pipeline = [
                # match artist spotify id
                {"$match": {
                    "spotify_id": str(artist_id)
                }},
                # sort by datetime
                {"$sort": {"datetime": 1}},
                # match date range
                {"$match": {
                    "datetime": {
                        "$lte": date_end,
                        "$gt": hundred_eighty_days_ago
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
                        "$round": [{"$multiply": [{"$divide": ["$follower", "$monthly_listener"]}, 100]}, 2]
                    }
                }}
            ]

                results = Spotify.objects().aggregate(pipeline)

                result = []
                for item in results:
                    result.append(item)
                # print(result)

                return jsonify({
                    'status': 'success',
                    'data': result
                }), 200
            elif (range == "365d"):
                year_ago = datetime.datetime.now() - datetime.timedelta(days=365)
                pipeline = [
                # match artist spotify id
                {"$match": {
                    "spotify_id": str(artist_id)
                }},
                # sort by datetime
                {"$sort": {"datetime": 1}},
                # match date range
                {"$match": {
                    "datetime": {
                        "$lte": date_end,
                        "$gt": year_ago
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
                        "$round": [{"$multiply": [{"$divide": ["$follower", "$monthly_listener"]}, 100]}, 2]
                    }
                }}
            ]

                results = Spotify.objects().aggregate(pipeline)

                result = []
                for item in results:
                    result.append(item)
                # print(result)

                return jsonify({
                    'status': 'success',
                    'data': result
                }), 200
            else:
                # calculate the date 7 days ago from today
                seven_days_ago = date_end - datetime.timedelta(days=7)

                pipeline = [
                # match artist spotify id
                {"$match": {
                    "spotify_id": str(artist_id)
                }},
                # sort by datetime
                {"$sort": {"datetime": 1}},
                # match date range
                {"$match": {
                    "datetime": {
                        "$lte": date_end,
                        "$gt": seven_days_ago
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
                        "$round": [{"$multiply": [{"$divide": ["$follower", "$monthly_listener"]}, 100]}, 2]
                    }
                }}
            ]

                results = Spotify.objects().aggregate(pipeline)

                result = []
                for item in results:
                    result.append(item)
                # print(result)

                return jsonify({
                    'status': 'success',
                    'data': result
                }), 200

        except Exception as e:
            return jsonify({
                'err': str(e)
            }), 500


# return spotify country charts
class SpotifyChartController:
    pass
