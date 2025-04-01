from models.sns.tiktok_model import Tiktok, TiktokVideo
import datetime

class TiktokController:

    # get most-used hashtags
    def get_hashtags_most_used_recent_ten(self):
        pass

    # get most-engaged hashtags
    def get_hashtags_most_engaged_recent_ten(self):
        pass

    def get_tiktok_follower(artist_id, date_end, range):
        format = "%Y-%m-%d"
        date_end = datetime.datetime.strptime(date_end, format)

        if (range == "7d"):
            # calculate the date 7 days ago from today
            seven_days_ago = date_end - datetime.timedelta(days=7)

            pipeline = [
                # match artist id
                {"$match": {
                    "id": artist_id
                }},
                {"$sort": {"datetime": 1}},
                # match date range
                {"$match": {
                    "datetime": {
                        "$lte": date_end,
                        "$gt": seven_days_ago
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
                    "follower": "$follower"
                }}
            ]

            results = Tiktok.objects().aggregate(pipeline)

            result = []
            for item in results:
                result.append(item)
            # print(result)

            return result
        elif (range == "28d"):
            # calculate the date 28 days ago from today
            twenty_eight_days_ago = datetime.datetime.now() - datetime.timedelta(days=28)

            pipeline = [
                # match artist id
                {"$match": {
                    "id": artist_id
                }},
                {"$sort": {"datetime": 1}},
                # match date range
                {"$match": {
                    "datetime": {
                        "$lte": date_end,
                        "$gt": twenty_eight_days_ago
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
                    "follower": "$follower"
                }}
            ]

            results = Tiktok.objects().aggregate(pipeline)

            result = []
            for item in results:
                result.append(item)
            # print(result)

            return result

        elif (range == "90d"):
            # calculate the date 90 days ago from today
            ninety_days_ago = datetime.datetime.now() - datetime.timedelta(days=90)

            pipeline = [
                # match artist id
                {"$match": {
                    "id": artist_id
                }},
                {"$sort": {"datetime": 1}},
                # match date range
                {"$match": {
                    "datetime": {
                        "$lte": date_end,
                        "$gt": ninety_days_ago
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
                    "follower": "$follower"
                }}
            ]

            results = Tiktok.objects().aggregate(pipeline)

            result = []
            for item in results:
                result.append(item)
            # print(result)

            return result

        elif (range == "180d"):
            # calculate the date 180 days ago from today
            hundred_eighty_days_ago = datetime.datetime.now() - datetime.timedelta(days=180)


            pipeline = [
                # match artist id
                {"$match": {
                    "id": artist_id
                }},
                {"$sort": {"datetime": 1}},
                # match date range
                {"$match": {
                    "datetime": {
                        "$lte": date_end,
                        "$gt": hundred_eighty_days_ago
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
                    "follower": "$follower"
                }}
            ]

            results = Tiktok.objects().aggregate(pipeline)

            result = []
            for item in results:
                result.append(item)
            # print(result)

            return result

        elif (range == "365d"):
            # calculate the date 180 days ago from today
            year_ago = datetime.datetime.now() - datetime.timedelta(days=365)

            pipeline = [
                # match artist id
                {"$match": {
                    "id": artist_id
                }},
                {"$sort": {"datetime": 1}},
                # match date range
                {"$match": {
                    "datetime": {
                        "$lte": date_end,
                        "$gt": year_ago
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
                    "follower": "$follower"
                }}
            ]

            results = Tiktok.objects().aggregate(pipeline)

            result = []
            for item in results:
                result.append(item)
            # print(result)

            return result

        else:
            # calculate the date 7 days ago from today
            seven_days_ago = date_end - datetime.timedelta(days=7)

            pipeline = [
                # match artist id
                {"$match": {
                    "id": artist_id
                }},
                {"$sort": {"datetime": 1}},
                # match date range
                {"$match": {
                    "datetime": {
                        "$lte": date_end,
                        "$gt": seven_days_ago
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
                    "follower": "$follower"
                }}
            ]

            results = Tiktok.objects().aggregate(pipeline)

            result = []
            for item in results:
                result.append(item)
            # print(result)

            return result

    def get_tiktok_hashtag(artist_id, date_end, range):
        format = "%Y-%m-%d"
        date_end = datetime.datetime.strptime(date_end, format)

        if (range == "7d"):
            # calculate the date 7 days ago from today
            seven_days_ago = date_end - datetime.timedelta(days=7)

            pipeline = [
                # match artist id
                {"$match": {
                    "id": artist_id
                }},
                {"$sort": {"datetime": 1}},
                # match date range
                {"$match": {
                    "datetime": {
                        "$lte": date_end,
                        "$gt": seven_days_ago
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
                    "hashtag": "$hashtag"
                }}
            ]

            results = Tiktok.objects().aggregate(pipeline)

            result = []
            for item in results:
                result.append(item)
            # print(result)

            return result

        elif (range == "28d"):
            # calculate the date 28 days ago from today
            twenty_eight_days_ago = datetime.datetime.now() - datetime.timedelta(days=28)

            pipeline = [
                # match artist id
                {"$match": {
                    "id": artist_id
                }},
                {"$sort": {"datetime": 1}},
                # match date range
                {"$match": {
                    "datetime": {
                        "$lte": date_end,
                        "$gt": twenty_eight_days_ago
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
                    "hashtag": "$hashtag"
                }}
            ]

            results = Tiktok.objects().aggregate(pipeline)

            result = []
            for item in results:
                result.append(item)
            # print(result)

            return result
        elif (range == "90d"):
            # calculate the date 90 days ago from today
            ninety_days_ago = datetime.datetime.now() - datetime.timedelta(days=90)

            pipeline = [
                # match artist id
                {"$match": {
                    "id": artist_id
                }},
                {"$sort": {"datetime": 1}},
                # match date range
                {"$match": {
                    "datetime": {
                        "$lte": date_end,
                        "$gt": ninety_days_ago
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
                    "hashtag": "$hashtag"
                }}
            ]

            results = Tiktok.objects().aggregate(pipeline)

            result = []
            for item in results:
                result.append(item)
            # print(result)

            return result
        elif (range == "180d"):
            # calculate the date 180 days ago from today
            hundred_eighty_days_ago = datetime.datetime.now() - datetime.timedelta(days=180)

            pipeline = [
                # match artist id
                {"$match": {
                    "id": artist_id
                }},
                {"$sort": {"datetime": 1}},
                # match date range
                {"$match": {
                    "datetime": {
                        "$lte": date_end,
                        "$gt": hundred_eighty_days_ago
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
                    "hashtag": "$hashtag"
                }}
            ]

            results = Tiktok.objects().aggregate(pipeline)

            result = []
            for item in results:
                result.append(item)
            # print(result)

            return result
        elif (range == "365d"):
            # calculate the date 180 days ago from today
            year_ago = datetime.datetime.now() - datetime.timedelta(days=365)

            pipeline = [
                # match artist id
                {"$match": {
                    "id": artist_id
                }},
                {"$sort": {"datetime": 1}},
                # match date range
                {"$match": {
                    "datetime": {
                        "$lte": date_end,
                        "$gt": year_ago
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
                    "hashtag": "$hashtag"
                }}
            ]

            results = Tiktok.objects().aggregate(pipeline)

            result = []
            for item in results:
                result.append(item)
            # print(result)

            return result
        else:
            # calculate the date 7 days ago from today
            seven_days_ago = date_end - datetime.timedelta(days=7)

            pipeline = [
                # match artist id
                {"$match": {
                    "id": artist_id
                }},
                {"$sort": {"datetime": 1}},
                # match date range
                {"$match": {
                    "datetime": {
                        "$lte": date_end,
                        "$gt": seven_days_ago
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
                    "hashtag": "$hashtag"
                }}
            ]

            results = Tiktok.objects().aggregate(pipeline)

            result = []
            for item in results:
                result.append(item)
            # print(result)

            return result

    def get_tiktok_like(artist_id, date_end, range):
        format = "%Y-%m-%d"
        date_end = datetime.datetime.strptime(date_end, format)

        if (range == "7d"):
            # calculate the date 7 days ago from today
            seven_days_ago = date_end - datetime.timedelta(days=7)

            pipeline = [
                # match artist id
                {"$match": {
                    "id": artist_id
                }},
                {"$sort": {"datetime": 1}},
                # match date range
                {"$match": {
                    "datetime": {
                        "$lte": date_end,
                        "$gt": seven_days_ago
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
                    "like": "$like"
                }}
            ]

            results = Tiktok.objects().aggregate(pipeline)

            result = []
            for item in results:
                result.append(item)
            # print(result)

            return result

        elif (range == "28d"):
            # calculate the date 28 days ago from today
            twenty_eight_days_ago = datetime.datetime.now() - datetime.timedelta(days=28)

            pipeline = [
                # match artist id
                {"$match": {
                    "id": artist_id
                }},
                {"$sort": {"datetime": 1}},
                # match date range
                {"$match": {
                    "datetime": {
                        "$lte": date_end,
                        "$gt": twenty_eight_days_ago
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
                    "like": "$like"
                }}
            ]

            results = Tiktok.objects().aggregate(pipeline)

            result = []
            for item in results:
                result.append(item)
            # print(result)

            return result
        elif (range == "90d"):
            # calculate the date 90 days ago from today
            ninety_days_ago = datetime.datetime.now() - datetime.timedelta(days=90)

            pipeline = [
                # match artist id
                {"$match": {
                    "id": artist_id
                }},
                {"$sort": {"datetime": 1}},
                # match date range
                {"$match": {
                    "datetime": {
                        "$lte": date_end,
                        "$gt": ninety_days_ago
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
                    "like": "$like"
                }}
            ]

            results = Tiktok.objects().aggregate(pipeline)

            result = []
            for item in results:
                result.append(item)
            # print(result)

            return result
        elif (range == "180d"):
            # calculate the date 180 days ago from today
            hundred_eighty_days_ago = datetime.datetime.now() - datetime.timedelta(days=180)

            pipeline = [
                # match artist id
                {"$match": {
                    "id": artist_id
                }},
                {"$sort": {"datetime": 1}},
                # match date range
                {"$match": {
                    "datetime": {
                        "$lte": date_end,
                        "$gt": hundred_eighty_days_ago
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
                    "like": "$like"
                }}
            ]

            results = Tiktok.objects().aggregate(pipeline)

            result = []
            for item in results:
                result.append(item)
            # print(result)

            return result
        elif (range == "365d"):
            # calculate the date 180 days ago from today
            year_ago = datetime.datetime.now() - datetime.timedelta(days=365)

            pipeline = [
                # match artist id
                {"$match": {
                    "id": artist_id
                }},
                {"$sort": {"datetime": 1}},
                # match date range
                {"$match": {
                    "datetime": {
                        "$lte": date_end,
                        "$gt": year_ago
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
                    "like": "$like"
                }}
            ]

            results = Tiktok.objects().aggregate(pipeline)

            result = []
            for item in results:
                result.append(item)
            # print(result)

            return result
        else:
            # calculate the date 7 days ago from today
            seven_days_ago = date_end - datetime.timedelta(days=7)

            pipeline = [
                # match artist id
                {"$match": {
                    "id": artist_id
                }},
                {"$sort": {"datetime": 1}},
                # match date range
                {"$match": {
                    "datetime": {
                        "$lte": date_end,
                        "$gt": seven_days_ago
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
                    "like": "$like"
                }}
            ]

            results = Tiktok.objects().aggregate(pipeline)

            result = []
            for item in results:
                result.append(item)
            # print(result)

            return result

    def get_tiktok_video_index(self):
        pass
