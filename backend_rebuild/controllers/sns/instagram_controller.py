from models.sns.instagram_model import Instagram
import datetime


class InstagramController:
    def get_follower(artist_id, date_end, range):
        """
        get instagram followers
        """
        format = "%Y-%m-%d"
        date_end = datetime.datetime.strptime(date_end, format)

        if (range == "7d"):
            # calculate the date 7 days ago from today
            seven_days_ago = date_end - datetime.timedelta(days=7)

            pipeline = [
                # match artist id
                {"$match": {
                    "user_id": artist_id
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
                    "follower": "$follower_count"
                }}
            ]

            results = Instagram.objects().aggregate(pipeline)

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
                    "user_id": artist_id
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
                    "follower": "$follower_count"
                }}
            ]

            results = Instagram.objects().aggregate(pipeline)

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
                    "user_id": artist_id
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
                    "follower": "$follower_count"
                }}
            ]

            results = Instagram.objects().aggregate(pipeline)

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
                    "user_id": artist_id
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
                    "follower": "$follower_count"
                }}
            ]

            results = Instagram.objects().aggregate(pipeline)

            result = []
            for item in results:
                result.append(item)
            # print(result)

            return result
        elif(range == "365d"):
            # calculate the date 180 days ago from today
            year_ago = datetime.datetime.now() - datetime.timedelta(days=365)
            pipeline = [
                # match artist id
                {"$match": {
                    "user_id": artist_id
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
                    "follower": "$follower_count"
                }}
            ]

            results = Instagram.objects().aggregate(pipeline)

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
                {"$project": {
                    "_id": 0,
                    "datetime": {
                        "$dateToString": {
                            "format": "%Y-%m-%d",
                            "date": "$datetime"
                        }
                    },
                    "follower": "$follower_count"
                }}
            ]

            results = Instagram.objects().aggregate(pipeline)

            result = []
            for item in results:
                result.append(item)
            # print(result)

            return result

    def get_post_count(artist_id, date_end, range):
        """
        get instagram media counts
        """
        format = "%Y-%m-%d"
        date_end = datetime.datetime.strptime(date_end, format)

        if (range == "7d"):
            # calculate the date 7 days ago from today
            seven_days_ago = date_end - datetime.timedelta(days=7)

            pipeline = [
                # match artist id
                {"$match": {
                    "user_id": artist_id
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
                    "posts_count": "$media_count"
                }}
            ]

            results = Instagram.objects().aggregate(pipeline)

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
                    "user_id": artist_id
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
                    "posts_count": "$media_count"
                }}
            ]

            results = Instagram.objects().aggregate(pipeline)

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
                    "user_id": artist_id
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
                    "posts_count": "$media_count"
                }}
            ]

            results = Instagram.objects().aggregate(pipeline)

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
                    "user_id": artist_id
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
                    "posts_count": "$media_count"
                }}
            ]

            results = Instagram.objects().aggregate(pipeline)

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
                    "user_id": artist_id
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
                    "posts_count": "$media_count"
                }}
            ]

            results = Instagram.objects().aggregate(pipeline)

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
                    "user_id": artist_id
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
                    "posts_count": "$media_count"
                }}
            ]

            results = Instagram.objects().aggregate(pipeline)

            result = []
            for item in results:
                result.append(item)
            # print(result)

            return result

    def get_threads_follower(artist_id, date_end, range):
        """
        Get Instagram threads follower
        :param date_end:
        :param range:
        :return:
        """
        format = "%Y-%m-%d"
        date_end = datetime.datetime.strptime(date_end, format)

        if (range == "7d"):
            # calculate the date 7 days ago from today
            seven_days_ago = date_end - datetime.timedelta(days=7)

            pipeline = [
                # match artist id
                {"$match": {
                    "user_id": artist_id
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
                    "threads_follower": "$threads_follower"
                }}
            ]

            results = Instagram.objects().aggregate(pipeline)

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
                    "user_id": artist_id
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
                    "threads_follower": "$threads_follower"
                }}
            ]

            results = Instagram.objects().aggregate(pipeline)

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
                    "user_id": artist_id
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
                    "threads_follower": "$threads_follower"
                }}
            ]

            results = Instagram.objects().aggregate(pipeline)

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
                    "user_id": artist_id
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
                    "threads_follower": "$threads_follower"
                }}
            ]

            results = Instagram.objects().aggregate(pipeline)

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
                    "user_id": artist_id
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
                    "threads_follower": "$threads_follower"
                }}
            ]

            results = Instagram.objects().aggregate(pipeline)

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
                    "user_id": artist_id
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
                    "threads_follower": "$threads_follower"
                }}
            ]

            results = Instagram.objects().aggregate(pipeline)

            result = []
            for item in results:
                result.append(item)
            # print(result)

            return result

    def get_likes(artist_id, range):
        """
        Get total likes & likes per post of the latest 12 posts
        :param range:
        :return:
        """

        if (range == "7d"):
            pipeline = [
                {"$match": {
                    "user_id": artist_id
                }},
                # sortby datetime
                {"$sort": {"datetime": 1}},
                # limit posts
                {"$limit": 7},
                {"$unwind": "$posts"},
                # return like fields
                {"$project": {
                    "_id": 0,
                    "datetime": {
                        "$dateToString": {
                            "format": "%Y-%m-%d",
                            "date": "$datetime"
                        }
                    },
                    "code": "$posts.code",
                    "like_count": "$posts.like_count"
                }},
                # group by date,
                # to calculate the total likes of latest 12 posts daily

                {"$group": {
                    "_id": "$datetime",
                    "code_list": {"$push": "$code"},
                    "post_count": {"$sum": 1},
                    "total_like": {"$sum": "$like_count"}
                }},
                # get likes per post
                {"$project": {
                    "_id": 0,
                    "datetime": "$_id",
                    "total_likes": "$total_like",
                    "like_per_post": {
                        "$round": [
                            {"$divide": ["$total_like", "$post_count"]}, 2
                        ]
                    }
                }}
            ]

            results = Instagram.objects().aggregate(pipeline)

            result = []
            for item in results:
                result.append(item)
            # print(result)

            return result
        elif (range == "28d"):
            pipeline = [
                {"$match": {
                    "user_id": artist_id
                }},
                # sortby datetime
                {"$sort": {"datetime": 1}},
                # limit posts
                {"$limit": 28},
                {"$unwind": "$posts"},
                # return like fields
                {"$project": {
                    "_id": 0,
                    "datetime": {
                        "$dateToString": {
                            "format": "%Y-%m-%d",
                            "date": "$datetime"
                        }
                    },
                    "code": "$posts.code",
                    "like_count": "$posts.like_count"
                }},
                # group by date,
                # to calculate the total likes of latest 12 posts daily

                {"$group": {
                    "_id": "$datetime",
                    "code_list": {"$push": "$code"},
                    "post_count": {"$sum": 1},
                    "total_like": {"$sum": "$like_count"}
                }},
                # get likes per post
                {"$project": {
                    "_id": 0,
                    "datetime": "$_id",
                    "total_likes": "$total_like",
                    "like_per_post": {
                        "$round": [
                            {"$divide": ["$total_like", "$post_count"]}, 2
                        ]
                    }
                }}
            ]

            results = Instagram.objects().aggregate(pipeline)

            result = []
            for item in results:
                result.append(item)
            # print(result)

            return result
        elif (range == "90d"):
            pipeline = [
                {"$match": {
                    "user_id": artist_id
                }},
                # sortby datetime
                {"$sort": {"datetime": 1}},
                # limit posts
                {"$limit": 90},
                {"$unwind": "$posts"},
                # return like fields
                {"$project": {
                    "_id": 0,
                    "datetime": {
                        "$dateToString": {
                            "format": "%Y-%m-%d",
                            "date": "$datetime"
                        }
                    },
                    "code": "$posts.code",
                    "like_count": "$posts.like_count"
                }},
                # group by date,
                # to calculate the total likes of latest 12 posts daily

                {"$group": {
                    "_id": "$datetime",
                    "code_list": {"$push": "$code"},
                    "post_count": {"$sum": 1},
                    "total_like": {"$sum": "$like_count"}
                }},
                # get likes per post
                {"$project": {
                    "_id": 0,
                    "datetime": "$_id",
                    "total_likes": "$total_like",
                    "like_per_post": {
                        "$round": [
                            {"$divide": ["$total_like", "$post_count"]}, 2
                        ]
                    }
                }}
            ]

            results = Instagram.objects().aggregate(pipeline)

            result = []
            for item in results:
                result.append(item)
            # print(result)

            return result
        else:
            pipeline = [
                {"$match": {
                    "user_id": artist_id
                }},
                # sortby datetime
                {"$sort": {"datetime": 1}},
                # limit posts
                {"$limit": 7},
                {"$unwind": "$posts"},
                # return like fields
                {"$project": {
                    "_id": 0,
                    "datetime": {
                        "$dateToString": {
                            "format": "%Y-%m-%d",
                            "date": "$datetime"
                        }
                    },
                    "code": "$posts.code",
                    "like_count": "$posts.like_count"
                }},
                # group by date,
                # to calculate the total likes of latest 12 posts daily

                {"$group": {
                    "_id": "$datetime",
                    "code_list": {"$push": "$code"},
                    "post_count": {"$sum": 1},
                    "total_like": {"$sum": "$like_count"}
                }},
                # get likes per post
                {"$project": {
                    "_id": 0,
                    "datetime": "$_id",
                    "total_likes": "$total_like",
                    "like_per_post": {
                        "$round": [
                            {"$divide": ["$total_like", "$post_count"]}, 2
                        ]
                    }
                }}
            ]

            results = Instagram.objects().aggregate(pipeline)

            result = []
            for item in results:
                result.append(item)
            # print(result)

            return result

    def get_comments(artist_id, range):

        if (range == "7d"):
            pipeline = [
                {"$match": {
                    "user_id": artist_id
                }},
                # sort by datetime
                {"$sort": {"datetime": 1}},
                # limit posts
                {"$limit": 7},
                {"$unwind": "$posts"},
                # return comment fields
                {"$project": {
                    "_id": 0,
                    "datetime": {
                        "$dateToString": {
                            "format": "%Y-%m-%d",
                            "date": "$datetime"
                        }
                    },
                    "code": "$posts.code",
                    "comment_count": "$posts.comment_count"
                }},
                # group by date,
                # to calculate the total likes of latest 12 posts daily
                {"$group": {
                    "_id": "$datetime",
                    "code_list": {"$push": "$code"},
                    "post_count": {"$sum": 1},
                    "total_comment": {"$sum": "$comment_count"}
                }},
                # get comments per post
                {"$project": {
                    "_id": 0,
                    "datetime": "$_id",
                    "total_comments": "$total_comment",
                    "comment_per_post": {
                        "$round": [
                            {"$divide": ["$total_comment", "$post_count"]}, 2
                        ]
                    }
                }}
            ]

            results = Instagram.objects().aggregate(pipeline)

            result = []
            for item in results:
                result.append(item)
            # print(result)

            return result
        elif (range == "28d"):
            pipeline = [
                {"$match": {
                    "user_id": artist_id
                }},
                # sort by datetime
                {"$sort": {"datetime": 1}},
                # limit posts
                {"$limit": 28},
                {"$unwind": "$posts"},
                # return comment fields
                {"$project": {
                    "_id": 0,
                    "datetime": {
                        "$dateToString": {
                            "format": "%Y-%m-%d",
                            "date": "$datetime"
                        }
                    },
                    "code": "$posts.code",
                    "comment_count": "$posts.comment_count"
                }},
                # group by date,
                # to calculate the total likes of latest 12 posts daily
                {"$group": {
                    "_id": "$datetime",
                    "code_list": {"$push": "$code"},
                    "post_count": {"$sum": 1},
                    "total_comment": {"$sum": "$comment_count"}
                }},
                # get comments per post
                {"$project": {
                    "_id": 0,
                    "datetime": "$_id",
                    "total_comments": "$total_comment",
                    "comment_per_post": {
                        "$round": [
                            {"$divide": ["$total_comment", "$post_count"]}, 2
                        ]
                    }
                }}
            ]

            results = Instagram.objects().aggregate(pipeline)

            result = []
            for item in results:
                result.append(item)
            # print(result)

            return result
        elif (range == "90d"):
            pipeline = [
                {"$match": {
                    "user_id": artist_id
                }},
                # sort by datetime
                {"$sort": {"datetime": 1}},
                # limit posts
                {"$limit": 90},
                {"$unwind": "$posts"},
                # return comment fields
                {"$project": {
                    "_id": 0,
                    "datetime": {
                        "$dateToString": {
                            "format": "%Y-%m-%d",
                            "date": "$datetime"
                        }
                    },
                    "code": "$posts.code",
                    "comment_count": "$posts.comment_count"
                }},
                # group by date,
                # to calculate the total likes of latest 12 posts daily
                {"$group": {
                    "_id": "$datetime",
                    "code_list": {"$push": "$code"},
                    "post_count": {"$sum": 1},
                    "total_comment": {"$sum": "$comment_count"}
                }},
                # get comments per post
                {"$project": {
                    "_id": 0,
                    "datetime": "$_id",
                    "total_comments": "$total_comment",
                    "comment_per_post": {
                        "$round": [
                            {"$divide": ["$total_comment", "$post_count"]}, 2
                        ]
                    }
                }}
            ]

            results = Instagram.objects().aggregate(pipeline)

            result = []
            for item in results:
                result.append(item)
            # print(result)

            return result
        else:
            pipeline = [
                {"$match": {
                    "user_id": artist_id
                }},
                # sort by datetime
                {"$sort": {"datetime": 1}},
                # limit posts
                {"$limit": 7},
                {"$unwind": "$posts"},
                # return comment fields
                {"$project": {
                    "_id": 0,
                    "datetime": {
                        "$dateToString": {
                            "format": "%Y-%m-%d",
                            "date": "$datetime"
                        }
                    },
                    "code": "$posts.code",
                    "comment_count": "$posts.comment_count"
                }},
                # group by date,
                # to calculate the total likes of latest 12 posts daily
                {"$group": {
                    "_id": "$datetime",
                    "code_list": {"$push": "$code"},
                    "post_count": {"$sum": 1},
                    "total_comment": {"$sum": "$comment_count"}
                }},
                # get comments per post
                {"$project": {
                    "_id": 0,
                    "datetime": "$_id",
                    "total_comments": "$total_comment",
                    "comment_per_post": {
                        "$round": [
                            {"$divide": ["$total_comment", "$post_count"]}, 2
                        ]
                    }
                }}
            ]

            results = Instagram.objects().aggregate(pipeline)

            result = []
            for item in results:
                result.append(item)
            # print(result)

            return result

    def get_posts_index(artist_id):
        """
        get instagram latest 12 posts index
        :param: artist_id
        :return:

        """
        pipeline = [
            # match artist
            {"$match": {
                "user_id": artist_id
            }},
            # sort by datetime
            {"$sort": {"datetime": -1}},
            {"$limit": 1},
            {"$unwind": "$posts"},
            # project
            {"$project": {
                "_id": 0,
                "datetime": "$datetime",
                "user_id": "$user_id",
                "pk": "$posts.pk",
                "username": "$posts.username",
                "code": "$posts.code",
                "taken_at": "$posts.taken_at",
                "media_type": "$posts.media_type",
                "product_type": "$posts.product_type",
                "comment_count": "$posts.comment_count",
                "like_count": "$posts.like_count",
                "play_count": "$posts.play_count",
                "view_count": "$posts.view_count",
                "caption_text": "$posts.caption_text",
                "thumbnail": "$posts.thumbnail",
                "video_url": "$posts.video_url"
            }},
            # lookup artist follower Number(
            {"$lookup": {
                "from": "instagram",
                "as": "ig_info",
                "let": {"user_idd": "$user_id"},
                "pipeline": [
                    {"$match": {
                        "$expr": {
                            "$eq": ["$user_id", "$$user_idd"]
                        }
                    }},
                    {"$sort": {"datetime": -1}},
                    {"$limit": 1}
                ]
            }},
            # unwind  ig_info
            {"$unwind": "$ig_info"},
            # project
            {"$project": {
                "_id": 0,
                "datetime": "$datetime",
                "user_id": "$user_id",
                "username": "$username",
                "taken_at": "$taken_at",
                "media_type": "$media_type",
                "product_type": "$product_type",
                "comment_count": "$comment_count",
                "like_count": "$like_count",
                "play_count": "$play_count",
                # "view_count": "$view_count",
                "caption_text": "$caption_text",
                "thumbnail": "$thumbnail",
                # "follower": "$ig_info.follower_count",
                "engagement_rate": {
                    "$round": [{
                        "$divide": [
                            {"$sum": ["$like_count", "$comment_count"]}, "$ig_info.follower_count"
                        ]}, 3]
                },
                "url": {
                    "$concat": [
                        "https://instagram.com/p/", "$code", "/"
                    ]
                }
            }}
        ]
        results = Instagram.objects().aggregate(pipeline)

        result = []
        for item in results:
            result.append(item)
        # print(result)

        return result

    def get_hashtags_most_engaged_recent_twelve(artist_id):
        pipeline = [
            {"$match": {
                "user_id": "242998577"
            }},
            {"$sort": {"datetime": -1}},
            {"$limit": 1},
            # lookup artist follower
            {"$lookup": {
                "from": "instagram",
                "as": "ig_info",
                "let": {"user_idd": "$user_id"},
                "pipeline": [
                    {"$match": {
                        "$expr": {
                            "$eq": ["$user_id", "$$user_idd"]
                        }
                    }},
                    {"$sort": {"datetime": -1}},
                    {"$limit": 1}
                ]
            }},
            {"$unwind": "$ig_info"},
            {"$unwind": "$posts"},
            {"$project": {
                "_id": 0,

                "hashtag": "$posts.hashtag",
                "eng_rate": {
                    "$round": [{
                        "$multiply": [
                            {"$divide": [
                                {"$sum": ["$posts.like_count", "$posts.comment_count"]}, "$ig_info.follower_count"
                            ]}, 100
                        ]
                    }, 3]
                }
            }},
            {"$unwind": "$hashtag"},
            {"$group": {
                "_id": "$hashtag",
                "count": {"$sum": 1},
                "eng_rate": {"$sum": "$eng_rate"}
            }},
            {"$project": {
                "eng_rate_per_hashtag": {
                    "$divide": ["$eng_rate", "$count"]
                }
            }},
            {"$sort": {"eng_rate_per_hashtag": -1}},
            {"$limit": 10}
        ]



    def get_hashtags_most_used_recent_twelve(self):
        pass

