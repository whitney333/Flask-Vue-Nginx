from models.sns.youtube_model import YoutubeVideo, Youtube
import pandas as pd
import numpy as np
import datetime


class YoutubeController:
    @staticmethod
    def extract_hashtags_keyword(text):
        """
        extract keywords with hashtag from string
        """
        # initializing hashtag_list variable
        hashtag_list = []

        # splitting the text into words
        for word in text.split():
            # checking the first character of every word
            if word[0] == '#':
                # adding the word to the hashtag_list
                hashtag_list.append(word[1:])
        return hashtag_list

    @classmethod
    #add this, if you need to call other functions in the same class
    def get_hashtags_most_used_recent_ten(self):

        pipeline = [
            # match artist channel id
            {"$match": {
                "channel_id": "UCcQ3rsk3vO-qaJkWYva5-KQ"
                # "UCAgiEbqDrziGMJ-h36t7ODg"
            }},
            {"$sort": {"datetime": -1}},
            {"$limit": 1},
            {"$unwind": "$video"},
            # get latest 10 posts
            {"$limit": 10},
            {"$project": {
                "_id": 0,
                "published_date": "$video.published_at",
                "title": "$video.title",
                "tags": "$video.tags"
            }},
            {"$set": {
                "n": {
                    "$replaceOne": {
                        "input": "$title",
                        "find": "#",
                        "replacement": " #"
                    }
                }
            }}
        ]

        results = Youtube.objects.aggregate(pipeline)


        _temp_list = []
        for item in results:
            _temp_list.append(item)

        # flatten item in list
        _tag = [ele.get("tags") for ele in _temp_list]
        _title = [self.extract_hashtags_keyword(ele["n"]) for ele in _temp_list]
        # print(_title)
        # print(_tag)
        flat_title = [item for sublist in _title for item in sublist]
        # print(flat_title)

        # replace None value to ''
        _switch_none = ['' if v is None else v for v in _tag]
        # flatten tags list
        flat_tag = [item for sublist in _switch_none for item in sublist]
        # print(flat_tag)

        # concatenate two lists, and count occurrence value
        joined_list = flat_title + flat_tag
        w = pd.value_counts(np.array(joined_list))

        # convert list to df then dict
        df = pd.DataFrame(list(zip(w.keys(), w)), columns=['_id', 'count'])
        result = df.to_dict(orient='records')[:10]

        response = {'result': result}
        # print(response)

        return response

    @classmethod
    def get_hashtags_mose_engaged_recent_ten(self):
        pass

    def get_subscribers(artist_id, date_end, range):
        """
        Get artist's subscribers count by different time range ()
        :return:
        """
        format = "%Y-%m-%d"
        date_end = datetime.datetime.strptime(date_end, format)

        if (range == "7d"):
            # calculate the date 7 days ago from today
            seven_days_ago = date_end - datetime.timedelta(days=7)

            pipeline = [
                # match artist channel id
                {"$match": {
                    "channel_id": artist_id
                }},
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
                    "subscriber_count": "$subscriber_count",
                }}
            ]

            results = Youtube.objects().aggregate(pipeline)

            result = []
            for item in results:
                result.append(item)
            # print(result)

            return result

        elif (range == "28d"):
            # calculate the date 28 days ago from today
            twenty_eight_days_ago = datetime.datetime.now() - datetime.timedelta(days=28)

            pipeline = [
                # match artist channel id
                {"$match": {
                    "channel_id": artist_id
                }},
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
                    "subscriber_count": "$subscriber_count",
                }}
            ]

            results = Youtube.objects().aggregate(pipeline)

            result = []
            for item in results:
                result.append(item)
            # print(result)

            return result

        elif (range == "90d"):
            # calculate the date 90 days ago from today
            ninety_days_ago = datetime.datetime.now() - datetime.timedelta(days=90)

            pipeline = [
                # match artist channel id
                {"$match": {
                    "channel_id": artist_id
                }},
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
                    "subscriber_count": "$subscriber_count",
                }}
            ]

            results = Youtube.objects().aggregate(pipeline)

            result = []
            for item in results:
                result.append(item)
            # print(result)

            return result

        elif (range == "180d"):
            # calculate the date 180 days ago from today
            hundred_eighty_days_ago = datetime.datetime.now() - datetime.timedelta(days=180)

            pipeline = [
                # match artist channel id
                {"$match": {
                    "channel_id": artist_id
                }},
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
                    "subscriber_count": "$subscriber_count",
                }}
            ]

            results = Youtube.objects().aggregate(pipeline)

            result = []
            for item in results:
                result.append(item)
            # print(result)

            return result

        elif (range == "365d"):
            # calculate the date 180 days ago from today
            year_ago = datetime.datetime.now() - datetime.timedelta(days=365)

            pipeline = [
                # match artist channel id
                {"$match": {
                    "channel_id": artist_id
                }},
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
                    "subscriber_count": "$subscriber_count",
                }}
            ]

            results = Youtube.objects().aggregate(pipeline)

            result = []
            for item in results:
                result.append(item)
            # print(result)

            return result

        else:
            # calculate the date 7 days ago from today
            seven_days_ago = date_end - datetime.timedelta(days=7)

            pipeline = [
                # match artist channel id
                {"$match": {
                    "channel_id": artist_id
                }},
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
                    "subscriber_count": "$subscriber_count",
                }}
            ]

            results = Youtube.objects().aggregate(pipeline)

            result = []
            for item in results:
                result.append(item)
            # print(result)

            return result

    def get_youtube_channel_view(artist_id, date_end, range):
        format = "%Y-%m-%d"
        date_end = datetime.datetime.strptime(date_end, format)

        if (range == "7d"):
            # calculate the date 7 days ago from today
            seven_days_ago = date_end - datetime.timedelta(days=7)

            pipeline = [
                # match artist channel id
                {"$match": {
                    "channel_id": artist_id
                }},
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
                    "view_count": "$view_count",
                }}
            ]

            results = Youtube.objects().aggregate(pipeline)

            result = []
            for item in results:
                result.append(item)
            # print(result)

            return result

        elif (range == "28d"):
            # calculate the date 28 days ago from today
            twenty_eight_days_ago = datetime.datetime.now() - datetime.timedelta(days=28)

            pipeline = [
                # match artist channel id
                {"$match": {
                    "channel_id": artist_id
                }},
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
                    "view_count": "$view_count",
                }}
            ]

            results = Youtube.objects().aggregate(pipeline)

            result = []
            for item in results:
                result.append(item)
            # print(result)

            return result

        elif (range == "90d"):
            # calculate the date 90 days ago from today
            ninety_days_ago = datetime.datetime.now() - datetime.timedelta(days=90)

            pipeline = [
                # match artist channel id
                {"$match": {
                    "channel_id": artist_id
                }},
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
                    "view_count": "$view_count",
                }}
            ]

            results = Youtube.objects().aggregate(pipeline)

            result = []
            for item in results:
                result.append(item)
            # print(result)

            return result

        elif (range == "180d"):
            # calculate the date 180 days ago from today
            hundred_eighty_days_ago = datetime.datetime.now() - datetime.timedelta(days=180)

            pipeline = [
                # match artist channel id
                {"$match": {
                    "channel_id": artist_id
                }},
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
                    "view_count": "$view_count",
                }}
            ]

            results = Youtube.objects().aggregate(pipeline)

            result = []
            for item in results:
                result.append(item)
            # print(result)

            return result

        elif (range == "365d"):
            # calculate the date 180 days ago from today
            year_ago = datetime.datetime.now() - datetime.timedelta(days=365)

            pipeline = [
                # match artist channel id
                {"$match": {
                    "channel_id": artist_id
                }},
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
                    "view_count": "$view_count",
                }}
            ]

            results = Youtube.objects().aggregate(pipeline)

            result = []
            for item in results:
                result.append(item)
            # print(result)

            return result

        else:
            # calculate the date 7 days ago from today
            seven_days_ago = date_end - datetime.timedelta(days=7)

            pipeline = [
                # match artist channel id
                {"$match": {
                    "channel_id": artist_id
                }},
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
                    "view_count": "$view_count",
                }}
            ]

            results = Youtube.objects().aggregate(pipeline)

            result = []
            for item in results:
                result.append(item)
            # print(result)

            return result

    @staticmethod
    def get_youtube_video_view():
        """
        get the latest 50 videos total views & avg views
        :return:
        """
        pass

    @staticmethod
    def get_youtube_video_like():
        """
        get the latest 50 videos total likes & avg likes
        :return:
        """
        pass

    @staticmethod
    def get_youtube_video_comment():
        pass

    def get_youtube_channel_hashtag(artist_id, date_end, range):
        format = "%Y-%m-%d"
        date_end = datetime.datetime.strptime(date_end, format)

        if (range == "7d"):
            # calculate the date 7 days ago from today
            seven_days_ago = date_end - datetime.timedelta(days=7)

            pipeline = [
                # match artist channel id
                {"$match": {
                    "channel_id": artist_id
                }},
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
                    "channel_hashtag": "$channel_hashtag",
                }}
            ]

            results = Youtube.objects().aggregate(pipeline)

            result = []
            for item in results:
                result.append(item)
            # print(result)

            return result

        elif (range == "28d"):
            # calculate the date 28 days ago from today
            twenty_eight_days_ago = datetime.datetime.now() - datetime.timedelta(days=28)

            pipeline = [
                # match artist channel id
                {"$match": {
                    "channel_id": artist_id
                }},
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
                    "channel_hashtag": "$channel_hashtag",
                }}
            ]

            results = Youtube.objects().aggregate(pipeline)

            result = []
            for item in results:
                result.append(item)
            # print(result)

            return result

        elif (range == "90d"):
            # calculate the date 90 days ago from today
            ninety_days_ago = datetime.datetime.now() - datetime.timedelta(days=90)

            pipeline = [
                # match artist channel id
                {"$match": {
                    "channel_id": artist_id
                }},
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
                    "channel_hashtag": "$channel_hashtag",
                }}
            ]

            results = Youtube.objects().aggregate(pipeline)

            result = []
            for item in results:
                result.append(item)
            # print(result)

            return result

        elif (range == "180d"):
            # calculate the date 180 days ago from today
            hundred_eighty_days_ago = datetime.datetime.now() - datetime.timedelta(days=180)

            pipeline = [
                # match artist channel id
                {"$match": {
                    "channel_id": artist_id
                }},
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
                    "channel_hashtag": "$channel_hashtag",
                }}
            ]

            results = Youtube.objects().aggregate(pipeline)

            result = []
            for item in results:
                result.append(item)
            # print(result)

            return result

        elif (range == "365d"):
            # calculate the date 180 days ago from today
            year_ago = datetime.datetime.now() - datetime.timedelta(days=365)

            pipeline = [
                # match artist channel id
                {"$match": {
                    "channel_id": artist_id
                }},
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
                    "channel_hashtag": "$channel_hashtag",
                }}
            ]

            results = Youtube.objects().aggregate(pipeline)

            result = []
            for item in results:
                result.append(item)
            # print(result)

            return result

        else:
            # calculate the date 7 days ago from today
            seven_days_ago = date_end - datetime.timedelta(days=7)

            pipeline = [
                # match artist channel id
                {"$match": {
                    "channel_id": artist_id
                }},
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
                    "channel_hashtag": "$channel_hashtag",
                }}
            ]

            results = Youtube.objects().aggregate(pipeline)

            result = []
            for item in results:
                result.append(item)
            # print(result)

            return result

    def get_youtube_video_hashtag(artist_id, date_end, range):
        format = "%Y-%m-%d"
        date_end = datetime.datetime.strptime(date_end, format)

        if (range == "7d"):
            # calculate the date 7 days ago from today
            seven_days_ago = date_end - datetime.timedelta(days=7)

            pipeline = [
                # match artist channel id
                {"$match": {
                    "channel_id": artist_id
                }},
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
                    "video_hashtag": "$video_hashtag"
                }}
            ]

            results = Youtube.objects().aggregate(pipeline)

            result = []
            for item in results:
                result.append(item)
            # print(result)

            return result

        elif (range == "28d"):
            # calculate the date 28 days ago from today
            twenty_eight_days_ago = datetime.datetime.now() - datetime.timedelta(days=28)

            pipeline = [
                # match artist channel id
                {"$match": {
                    "channel_id": artist_id
                }},
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
                    "video_hashtag": "$video_hashtag"
                }}
            ]

            results = Youtube.objects().aggregate(pipeline)

            result = []
            for item in results:
                result.append(item)
            # print(result)

            return result

        elif (range == "90d"):
            # calculate the date 90 days ago from today
            ninety_days_ago = datetime.datetime.now() - datetime.timedelta(days=90)

            pipeline = [
                # match artist channel id
                {"$match": {
                    "channel_id": artist_id
                }},
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
                    "video_hashtag": "$video_hashtag"
                }}
            ]

            results = Youtube.objects().aggregate(pipeline)

            result = []
            for item in results:
                result.append(item)
            # print(result)

            return result

        elif (range == "180d"):
            # calculate the date 180 days ago from today
            hundred_eighty_days_ago = datetime.datetime.now() - datetime.timedelta(days=180)

            pipeline = [
                # match artist channel id
                {"$match": {
                    "channel_id": artist_id
                }},
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
                    "video_hashtag": "$video_hashtag"
                }}
            ]

            results = Youtube.objects().aggregate(pipeline)

            result = []
            for item in results:
                result.append(item)
            # print(result)

            return result

        elif (range == "365d"):
            # calculate the date 180 days ago from today
            year_ago = datetime.datetime.now() - datetime.timedelta(days=365)

            pipeline = [
                # match artist channel id
                {"$match": {
                    "channel_id": artist_id
                }},
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
                    "video_hashtag": "$video_hashtag"
                }}
            ]

            results = Youtube.objects().aggregate(pipeline)

            result = []
            for item in results:
                result.append(item)
            # print(result)

            return result

        else:
            # calculate the date 7 days ago from today
            seven_days_ago = date_end - datetime.timedelta(days=7)

            pipeline = [
                # match artist channel id
                {"$match": {
                    "channel_id": artist_id
                }},
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
                    "video_hashtag": "$video_hashtag"
                }}
            ]

            results = Youtube.objects().aggregate(pipeline)

            result = []
            for item in results:
                result.append(item)
            # print(result)

            return result
