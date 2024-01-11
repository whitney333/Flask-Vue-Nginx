from models import main_db
from flask import jsonify, Blueprint
from bson.json_util import dumps
import datetime
from datetime import timedelta
from flask_restful import Resource, reqparse, Api


tiktok_api_bp = Blueprint('tiktok_api', __name__)
tiktok_api = Api(tiktok_api_bp)


@tiktok_api_bp.route('/tiktok/chart/follower', methods=['GET'])
def get_tiktok_video():
    try:
        result = main_db.tiktok_index.aggregate([
            {"$sort": {"datetime": -1}},
            {"$project": {
                "_id": 0,
                "datetime": {
                    "$dateToString": {
                        "format": "%Y-%m-%d",
                        "date": "$datetime"
                    }
                },
                "tiktok_follower": "$tiktok_follower",
                "tiktok_like": "$tiktok_like"
            }},
            {"$sort": {"datetime": 1}}
        ])
        return dumps({"result": result})
    except Exception as e:
        return jsonify(str(e))

@tiktok_api_bp.route('/tiktok/average-index', methods=['GET'])
def get_tiktok_avg_index():
    try:
        index = main_db.tiktok_video_info.aggregate([
            {"$sort": {"datetime": -1}},
            {"$limit": 1},
            {"$unwind": "$data"},
            {"$project": {
                "_id": 0,
                "datetime": {
                    "$dateToString": {
                        "format": "%Y-%m-%d",
                        "date": "$datetime"
                    }
                },
                "comment": "$data.comment",
                "like": "$data.like",
                "share": "$data.new_share",
                "views": "$data.views"

            }},
            {"$group": {
                "_id": "index",
                "video_num": {"$sum": 1},
                "total_like": {"$sum": "$like"},
                "total_comment": {"$sum": "$comment"},
                "total_share": {"$sum": "$share"},
                "total_views": {"$sum": "$views"}
            }}
        ])

        past_week_index = main_db.tiktok_video_info.aggregate([
            {"$sort": {"datetime": -1}},
            {"$skip": 1},
            {"$limit": 1},
            {"$unwind": "$data"},
            {"$project": {
                "_id": 0,
                "datetime": {
                    "$dateToString": {
                        "format": "%Y-%m-%d",
                        "date": "$datetime"
                    }
                },
                "comment": "$data.comment",
                "like": "$data.like",
                "share": "$data.new_share",
                "views": "$data.views"

            }},
            {"$group": {
                "_id": "index",
                "video_num": {"$sum": 1},
                "total_like": {"$sum": "$like"},
                "total_comment": {"$sum": "$comment"},
                "total_share": {"$sum": "$share"},
                "total_views": {"$sum": "$views"}
            }}
        ])

        return dumps({"current_total": index,
                      "past_week_total": past_week_index})
    except Exception as e:
        return dumps({'error': str(e)})

@tiktok_api_bp.route('/tiktok/chart', methods=['GET'])
def get_tiktok_index():
    try:
        result = main_db.tiktok_video_info.aggregate([
            {"$sort": {"datetime": -1}},
            {"$unwind": "$data"},
            {"$project": {
                "_id": 0,
                "datetime": {
                    "$dateToString": {
                        "format": "%Y-%m-%d",
                        "date": "$datetime"
                    }
                },
                "title": "$data.title",
                "views": "$data.views",
                "likes": "$data.like",
                "comments": "$data.comment",
                "shares": "$data.new_share",
                "saves": "$data.save"
            }},
            {"$group": {
                "_id": "$datetime",
                "video_num": {"$sum": {"$toInt": 1}},
                "total_view": {"$sum": "$views"},
                "total_like": {"$sum": "$likes"},
                "total_comment": {"$sum": "$comments"},
                "total_share": {"$sum": "$shares"},
                "total_save": {"$sum": "$saves"}
            }},
            {"$sort": {"_id": 1}},
            {"$addFields": {
                "sub_total": {
                    "$sum": ["$total_like", "$total_comment", "$total_share", "$total_save"]}
            }},
            {"$project": {
                "datetime": "$_id",
                "video_num": "$video_num",
                "eng_rate": {
                    "$round": [
                        {"$multiply": [{"$divide": ["$sub_total", "$total_view"]}, 100]}, 2
                    ]
                },
                "total_like": "$total_like",
                "total_comment": "$total_comment",
                "total_share": "$total_share",
                "total_views": "$total_view",
                "total_save": "$total_save",
                "avg_like": {
                    "$round": [{"$divide": ["$total_like", "$video_num"]}, 2]
                },
                "avg_comment": {
                    "$round": [{"$divide": ["$total_comment", "$video_num"]}, 2]
                },
                "avg_share": {
                    "$round": [{"$divide": ["$total_share", "$video_num"]}, 2]
                },
                "avg_view": {
                    "$round": [{"$divide": ["$total_view", "$video_num"]}, 2]
                },
                "avg_save": {
                    "$round": [{"$divide": ["$total_save", "$video_num"]}, 2]
                }
            }}
        ])
        return dumps({'result': result})
    except Exception as e:
        return dumps({'error': str(e)})

@tiktok_api_bp.route('/tiktok/hashtags/most-used/recent-ten-posts', methods=['GET'])
def get_hashtags_recent_ten():
    try:
        result = main_db.tiktok_video_info.aggregate([
            {"$sort": {"datetime": -1}},
            {"$limit": 1},
            {"$unwind": "$data"},
            {"$limit": 10},
            {"$project": {
                "hashtags": "$data.hashtags",
                "_id": 0
            }},
            {"$unwind": "$hashtags"},
            {"$group":
                 {"_id": "$hashtags", "count": {"$sum": 1}}
             },
            {"$sort": {"count": -1}},
            {"$limit": 10}
        ])
        return dumps({'result': result})
    except Exception as e:
        return dumps({'err': str(e)})

@tiktok_api_bp.route('/tiktok/hashtags/most-used/recent-thirty-posts', methods=['GET'])
def get_hashtags_recent_thirty():
    try:
        result = main_db.tiktok_video_info.aggregate([
            {"$sort": {"datetime": -1}},
            {"$limit": 1},
            {"$unwind": "$data"},
            {"$limit": 30},
            {"$project": {
                "hashtags": "$data.hashtags",
                "_id": 0
            }},
            {"$unwind": "$hashtags"},
            {"$group":
                 {"_id": "$hashtags", "count": {"$sum": 1}}
             },
            {"$sort": {"count": -1}},
            {"$limit": 10}
        ])
        return dumps({'result': result})
    except Exception as e:
        return dumps({'err': str(e)})

@tiktok_api_bp.route('/tiktok/hashtags/most-used/overall-posts', methods=['GET'])
def get_hashtags_most_used_overall():
    try:
        result = main_db.tiktok_video_info.aggregate([
            {"$sort": {"datetime": -1}},
            {"$limit": 1},
            {"$unwind": "$data"},
            {"$project": {
                "hashtags": "$data.hashtags",
                "_id": 0
            }},
            {"$unwind": "$hashtags"},
            {"$group":
                 {"_id": "$hashtags", "count": {"$sum": 1}}
             },
            {"$sort": {"count": -1}},
            {"$limit": 10}
        ])
        return dumps({'result': result})
    except Exception as e:
        return dumps({'err': str(e)})

@tiktok_api_bp.route('/tiktok/hashtags/most-engaged/recent-ten-posts', methods=['GET'])
def get_most_engaged_hashtags_recent_ten():
    try:
        result = main_db.tiktok_video_info.aggregate([
            {"$sort": {"datetime": -1}},
            {"$limit": 1},
            {"$unwind": "$data"},
            {"$addFields": {
                "sub_total": {
                    "$sum": ["$data.comment", "$data.like", "$data.new_share"]}
            }},
            {"$project": {
                "_id": 0,
                "post_date": "$data.new_show_date",
                "views": "$data.views",
                "hashtags": "$data.hashtags",
                "sub_total": "$sub_total"
            }},
            {"$limit": 10},
            {"$unwind": "$hashtags"},
            {"$addFields": {
                "_eng_rate": {"$divide": ["$sub_total", "$views"]}
            }},
            {"$group": {
                "_id": "$hashtags",
                "count": {"$sum": 1},
                "_total_eng_rate": {"$sum": "$_eng_rate"}
            }},
            {"$project": {
                "eng_rate_per_hashtag": {
                    "$divide": ["$_total_eng_rate", "$count"]
                }
            }},
            {"$project": {
                "eng_rate_per_hashtag": {
                    "$round": [{"$multiply": ["$eng_rate_per_hashtag", 100]}, 2]
                }
            }},
            {"$sort": {"eng_rate_per_hashtag": -1}},
            {"$limit": 10}
        ])
        return dumps({'result': result})
    except Exception as e:
        return dumps({'err': str(e)})

@tiktok_api_bp.route('/tiktok/hashtags/most-engaged/recent-thirty-posts', methods=['GET'])
def get_most_engaged_hashtags_recent_thirty():
    try:
        result = main_db.tiktok_video_info.aggregate([
            {"$sort": {"datetime": -1}},
            {"$limit": 1},
            {"$unwind": "$data"},
            {"$addFields": {
                 "sub_total": {
                    "$sum": ["$data.comment", "$data.like", "$data.new_share"]}
            }},
            {"$project": {
                "_id": 0,
                "post_date": "$data.new_show_date",
                "views": "$data.views",
                "hashtags": "$data.hashtags",
                "sub_total": "$sub_total"
            }},
            {"$limit": 30},
            {"$unwind": "$hashtags"},
            {"$addFields": {
                "_eng_rate": {"$divide": ["$sub_total", "$views"]}
            }},
            {"$group": {
                "_id": "$hashtags",
                "count": {"$sum": 1},
                "_total_eng_rate": {"$sum": "$_eng_rate"}
            }},
            {"$project": {
                "eng_rate_per_hashtag": {
                    "$divide": ["$_total_eng_rate", "$count"]
                }
            }},
            {"$project": {
                "eng_rate_per_hashtag": {
                    "$round": [{"$multiply": ["$eng_rate_per_hashtag", 100]}, 2]
                }
            }},
            {"$sort": {"eng_rate_per_hashtag": -1}},
            {"$limit": 10}
        ])
        return dumps({'result': result})
    except Exception as e:
        return dumps({'err': str(e)})

@tiktok_api_bp.route('/tiktok/hashtags/most-engaged/overall-posts', methods=['GET'])
def get_most_engaged_hashtags_overall():
    try:
        result = main_db.tiktok_video_info.aggregate([
            {"$sort": {"datetime": -1}},
            {"$limit": 1},
            {"$unwind": "$data"},
            {"$addFields": {
                 "sub_total": {
                    "$sum": ["$data.comment", "$data.like", "$data.new_share"]}
            }},
            {"$project": {
                "_id": 0,
                "post_date": "$data.new_show_date",
                "views": "$data.views",
                "hashtags": "$data.hashtags",
                "sub_total": "$sub_total"
            }},
            {"$unwind": "$hashtags"},
            {"$addFields": {
                "_eng_rate": {"$divide": ["$sub_total", "$views"]}
            }},
            {"$group": {
                "_id": "$hashtags",
                "count": {"$sum": 1},
                "_total_eng_rate": {"$sum": "$_eng_rate"}
            }},
            {"$project": {
                "eng_rate_per_hashtag": {
                    "$divide": ["$_total_eng_rate", "$count"]
                }
            }},
            {"$project": {
                "eng_rate_per_hashtag": {
                    "$round": [{"$multiply": ["$eng_rate_per_hashtag", 100]}, 2]
                }
            }},
            {"$sort": {"eng_rate_per_hashtag": -1}},
            {"$limit": 10}
        ])
        return dumps({'result': result})
    except Exception as e:
        return dumps({'err': str(e)})

class TiktokPost(Resource):
    def get(self):
        posts_data = reqparse.RequestParser()
        posts_data.add_argument('page', type=str, required=True, help='Page number is required', location='args')
        posts_data.add_argument('limit', type=str, required=True, help='Limit is required', location='args')
        posts_data.add_argument('sort', type=str, required=False, location='args')
        data = posts_data.parse_args()

        page = data['page']
        page_limit = data['limit']
        sort = data['sort']
        _temp_list = []

        # Total number of posts
        posts_count_cur = main_db.tiktok_video_info.aggregate([
            {"$sort": {"datetime": -1}},
            {"$limit": 1},
            {"$unwind": "$data"},
            {"$group": {"_id": "total", "count": {"$sum": {"$toInt": 1}}}}
        ])

        for item in posts_count_cur:
            _temp_list.append(item['count'])

        posts_count = _temp_list[0]

        # Sort By: Date/ Most Likes/ Most Comments
        # case 1: Date
        if (sort == 'date'):
            fetch_posts = main_db.tiktok_video_info.aggregate([
                {"$sort": {"datetime": -1}},
                {"$limit": 1},
                {"$unwind": "$data"},
                {"$addFields": {
                    "sub_total": {
                        "$sum": ["$data.like", "$data.comment", "$data.new_share"]
                    }
                }},
                {"$addFields": {
                    "eng_rate": {
                        "$divide": ["$sub_total", "$data.views"]
                    }
                }},
                {"$project": {
                    "_id": 0,
                    "publish_at": {
                        "$dateToString": {
                            "format": "%Y-%m-%d",
                            "date": "$data.new_show_date"
                        }
                    },
                    "views": "$data.views",
                    "likes": "$data.like",
                    "share": "$data.new_share",
                    "comments": "$data.comment",
                    "eng_rate": {
                        "$multiply": ["$eng_rate", 100]
                    },
                    "hashtags": "$data.hashtags",
                    "url": "$data.url",
                    "image": "$data.new_image_url"
                }},
                {"$sort": {"publish_at": -1}},
                {"$skip": int(page_limit) * (int(page) - 1)},
                {"$limit": int(page_limit)}
            ])

            posts_list = []
            for post in fetch_posts:
                posts_list.append(post)

            response = {'total_posts_count': posts_count, 'page': int(page), 'perPage': int(page_limit), 'sort': sort, 'posts': posts_list}

            return {'result': response}

        elif (sort == 'like'):
            fetch_posts = main_db.tiktok_video_info.aggregate([
                {"$sort": {"datetime": -1}},
                {"$limit": 1},
                {"$unwind": "$data"},
                {"$addFields": {
                    "sub_total": {
                        "$sum": ["$data.like", "$data.comment", "$data.new_share"]
                    }
                }},
                {"$addFields": {
                    "eng_rate": {
                        "$divide": ["$sub_total", "$data.views"]
                    }
                }},
                {"$project": {
                    "_id": 0,
                    "publish_at": {
                        "$dateToString": {
                            "format": "%Y-%m-%d",
                            "date": "$data.new_show_date"
                        }
                    },
                    "views": "$data.views",
                    "likes": "$data.like",
                    "share": "$data.new_share",
                    "comments": "$data.comment",
                    "eng_rate": {
                        "$multiply": ["$eng_rate", 100]
                    },
                    "hashtags": "$data.hashtags",
                    "url": "$data.url",
                    "image": "$data.new_image_url"
                }},
                {"$sort": {"likes": -1}},
                {"$skip": int(page_limit) * (int(page) - 1)},
                {"$limit": int(page_limit)}
            ])

            posts_list = []
            for post in fetch_posts:
                posts_list.append(post)

            response = {'total_posts_count': posts_count, 'page': int(page), 'perPage': int(page_limit), 'sort': sort, 'posts': posts_list}

            return {'result': response}

        elif (sort == 'comment'):
            fetch_posts = main_db.tiktok_video_info.aggregate([
                {"$sort": {"datetime": -1}},
                {"$limit": 1},
                {"$unwind": "$data"},
                {"$addFields": {
                    "sub_total": {
                        "$sum": ["$data.like", "$data.comment", "$data.new_share"]
                    }
                }},
                {"$addFields": {
                    "eng_rate": {
                        "$divide": ["$sub_total", "$data.views"]
                    }
                }},
                {"$project": {
                    "_id": 0,
                    "publish_at": {
                        "$dateToString": {
                            "format": "%Y-%m-%d",
                            "date": "$data.new_show_date"
                        }
                    },
                    "views": "$data.views",
                    "likes": "$data.like",
                    "share": "$data.new_share",
                    "comments": "$data.comment",
                    "eng_rate": {
                        "$multiply": ["$eng_rate", 100]
                    },
                    "hashtags": "$data.hashtags",
                    "url": "$data.url",
                    "image": "$data.new_image_url"
                }},
                {"$sort": {"comments": -1}},
                {"$skip": int(page_limit) * (int(page) - 1)},
                {"$limit": int(page_limit)}
            ])

            posts_list = []
            for post in fetch_posts:
                posts_list.append(post)

            response = {'total_posts_count': posts_count, 'page': int(page), 'perPage': int(page_limit), 'sort': sort, 'posts': posts_list}

            return {'result': response}

        elif (sort == 'engaged'):
            fetch_posts = main_db.tiktok_video_info.aggregate([
                {"$sort": {"datetime": -1}},
                {"$limit": 1},
                {"$unwind": "$data"},
                {"$addFields": {
                    "sub_total": {
                        "$sum": ["$data.like", "$data.comment", "$data.new_share"]
                    }
                }},
                {"$addFields": {
                    "eng_rate": {
                        "$divide": ["$sub_total", "$data.views"]
                    }
                }},
                {"$project": {
                    "_id": 0,
                    "publish_at": {
                        "$dateToString": {
                            "format": "%Y-%m-%d",
                            "date": "$data.new_show_date"
                        }
                    },
                    "views": "$data.views",
                    "likes": "$data.like",
                    "share": "$data.new_share",
                    "comments": "$data.comment",
                    "eng_rate": {
                        "$multiply": ["$eng_rate", 100]
                    },
                    "hashtags": "$data.hashtags",
                    "url": "$data.url",
                    "image": "$data.new_image_url"
                }},
                {"$sort": {"eng_rate": -1}},
                {"$skip": int(page_limit) * (int(page) - 1)},
                {"$limit": int(page_limit)}
            ])

            posts_list = []
            for post in fetch_posts:
                posts_list.append(post)

            response = {'total_posts_count': posts_count, 'page': int(page), 'perPage': int(page_limit), 'sort': sort, 'posts': posts_list}

            return {'result': response}

        elif (sort == 'view'):
            fetch_posts = main_db.tiktok_video_info.aggregate([
                {"$sort": {"datetime": -1}},
                {"$limit": 1},
                {"$unwind": "$data"},
                {"$addFields": {
                    "sub_total": {
                        "$sum": ["$data.like", "$data.comment", "$data.new_share"]
                    }
                }},
                {"$addFields": {
                    "eng_rate": {
                        "$divide": ["$sub_total", "$data.views"]
                    }
                }},
                {"$project": {
                    "_id": 0,
                    "publish_at": {
                        "$dateToString": {
                            "format": "%Y-%m-%d",
                            "date": "$data.new_show_date"
                        }
                    },
                    "views": "$data.views",
                    "likes": "$data.like",
                    "share": "$data.new_share",
                    "comments": "$data.comment",
                    "eng_rate": {
                        "$multiply": ["$eng_rate", 100]
                    },
                    "hashtags": "$data.hashtags",
                    "url": "$data.url",
                    "image": "$data.new_image_url"
                }},
                {"$sort": {"views": -1}},
                {"$skip": int(page_limit) * (int(page) - 1)},
                {"$limit": int(page_limit)}
            ])

            posts_list = []
            for post in fetch_posts:
                posts_list.append(post)

            response = {'total_posts_count': posts_count, 'page': int(page), 'perPage': int(page_limit), 'sort': sort, 'posts': posts_list}

            return {'result': response}

        elif (sort == 'share'):
            fetch_posts = main_db.tiktok_video_info.aggregate([
                {"$sort": {"datetime": -1}},
                {"$limit": 1},
                {"$unwind": "$data"},
                {"$addFields": {
                    "sub_total": {
                        "$sum": ["$data.like", "$data.comment", "$data.new_share"]
                    }
                }},
                {"$addFields": {
                    "eng_rate": {
                        "$divide": ["$sub_total", "$data.views"]
                    }
                }},
                {"$project": {
                    "_id": 0,
                    "publish_at": {
                        "$dateToString": {
                            "format": "%Y-%m-%d",
                            "date": "$data.new_show_date"
                        }
                    },
                    "views": "$data.views",
                    "likes": "$data.like",
                    "share": "$data.new_share",
                    "comments": "$data.comment",
                    "eng_rate": {
                        "$multiply": ["$eng_rate", 100]
                    },
                    "hashtags": "$data.hashtags",
                    "url": "$data.url",
                    "image": "$data.new_image_url"
                }},
                {"$sort": {"share": -1}},
                {"$skip": int(page_limit) * (int(page) - 1)},
                {"$limit": int(page_limit)}
            ])

            posts_list = []
            for post in fetch_posts:
                posts_list.append(post)

            response = {'total_posts_count': posts_count, 'page': int(page), 'perPage': int(page_limit), 'sort': sort, 'posts': posts_list}

            return {'result': response}
        else:
            fetch_posts = main_db.tiktok_video_info.aggregate([
                {"$sort": {"datetime": -1}},
                {"$limit": 1},
                {"$unwind": "$data"},
                {"$addFields": {
                    "sub_total": {
                        "$sum": ["$data.like", "$data.comment", "$data.new_share"]
                    }
                }},
                {"$addFields": {
                    "eng_rate": {
                        "$divide": ["$sub_total", "$data.views"]
                    }
                }},
                {"$project": {
                    "_id": 0,
                    "publish_at": {
                        "$dateToString": {
                            "format": "%Y-%m-%d",
                            "date": "$data.new_show_date"
                        }
                    },
                    "views": "$data.views",
                    "likes": "$data.like",
                    "share": "$data.new_share",
                    "comments": "$data.comment",
                    "eng_rate": {
                        "$multiply": ["$eng_rate", 100]
                    },
                    "hashtags": "$data.hashtags",
                    "url": "$data.url",
                    "image": "$data.new_image_url"
                }},
                {"$sort": {"publish_at": -1}},
                {"$skip": int(page_limit) * (int(page) - 1)},
                {"$limit": int(page_limit)}
            ])

            posts_list = []
            for post in fetch_posts:
                posts_list.append(post)

            response = {'total_posts_count': posts_count, 'page': int(page), 'perPage': int(page_limit), 'sort': sort, 'posts': posts_list}

            return {'result': response}
