from models import main_db
from flask import jsonify, Blueprint
from bson.json_util import dumps
import datetime
from datetime import timedelta
from flask_restful import Resource, reqparse, Api


instagram_api_bp = Blueprint('instagram_api', __name__)
instagram_api = Api(instagram_api_bp)

@instagram_api_bp.route('/instagram/chart/follower', methods=['GET'])
def get_instagram_follower_chart():
    try:
        result = main_db.instagram_user_info.aggregate([
            {"$sort": {"date": 1}},
            {"$project": {
                "_id": 0,
                "datetime": {
                    "$dateToString": {
                        "format": "%Y-%m-%d",
                        "date": "$date"
                    }},
                "user": "$username",
                "media_count": "$media_count",
                "follower_count": "$follower_count"
            }}
        ])
        return dumps({'result': result})
    except Exception as e:
        return dumps({'error': str(e)})

@instagram_api_bp.route('/instagram/chart', methods=['GET'])
def get_instagram_chart_index():
    try:
        result = main_db.instagram_post_info.aggregate([
            {"$sort": {"date": -1}},
            {"$project": {
                "_id": 0,
                "date": "$date",
                "media_count": "$media_count",
                "follower_count": "$follower_count",
                "post": {"$slice": ["$post", 0, 12]}
            }},
            {"$unwind": "$post"},
            {"$project": {
                "_id": 0,
                "datetime": {
                    "$dateToString": {
                        "format": "%Y-%m-%d",
                        "date": "$date"
                    }
                },
                "taken_at": "$post.taken_at",
                "follower": "$follower_count",
                "text": "$post.caption_text",
                "hashtags": "$post.hashtags",
                "comments": "$post.comment_count",
                "likes": "$post.like_count",
                "views": "$post.view_count"
            }},
            {"$group": {
                "_id": "$datetime",
                "follower": {"$first": "$follower"},
                "post_num": {"$sum": {"$toInt": 1}},
                "total_view": {"$sum": "$views"},
                "total_comment": {"$sum": "$comments"},
                "total_like": {"$sum": "$likes"},
            }},
            {"$sort": {"_id": 1}},
            {"$addFields": {
                "sub_total": {
                    "$sum": ["$total_like", "$total_comment"]
                }
            }},
            {"$project": {
                "datetime": "$_id",
                "follower": "$follower",
                "post_num": "$post_num",
                "total_like": "$total_like",
                "total_comment": "$total_comment",
                "total_view": "$total_view",
                "avg_like": {
                    "$round": [{"$divide": ["$total_like", "$post_num"]}, 2]
                },
                "avg_comment": {
                    "$round": [{"$divide": ["$total_comment", "$post_num"]}, 2]
                }
            }},
            {"$addFields": {
                "avg_sub_total": {
                    "$sum": ["$avg_like", "$avg_comment"]
                }
            }},
            {"$project": {
                "datetime": "$_id",
                "post_num": "$post_num",
                "eng_rate": {
                    "$round": [
                        {"$multiply": [{"$divide": ["$avg_sub_total", "$follower"]}, 100]}, 2
                    ]
                },
                "total_like": "$total_like",
                "total_comment": "$total_comment",
                "total_view": "$total_view",
                "avg_like": "$avg_like",
                "avg_comment": "$avg_comment"
            }}
        ], allowDiskUse=True)
        return dumps({'result': result})
    except Exception as e:
        return dumps({'err': str(e)})

@instagram_api_bp.route('/instagram/index', methods=['GET'])
def get_instagram_index():
    try:
        main_index = main_db.instagram_user_info.aggregate([
            {"$sort": {"date": -1}},
            {"$limit": 7},
            {"$project": {
                "_id": 0,
                "date": {
                    "$dateToString": {
                        "format": "%Y-%m-%d",
                        "date": "$date"
                    }},
                "media_count": "$media_count",
                "follower_count": "$follower_count",
                "following_count": "$following_count",
            }}
        ])
        return dumps({"result": main_index}), 200
    except Exception as e:
        return jsonify(str(e)), 404

@instagram_api_bp.route('/instagram/threads/follower', methods=['GET'])
def get_instagram_threads_follower():
    try:
        result = main_db.instagram_threads.aggregate([
            {"$sort": {"date": 1}},
            {"$project": {
                "_id": 0,
                "datetime": {
                    "$dateToString": {
                        "format": "%Y-%m-%d",
                        "date": "$date"
                    }},
                "threads_followers": "$follower_count"
            }}
        ])
        return dumps({'result': result})
    except Exception as e:
        return dumps({'error': (e)})

# instagram most-used hashtags
@instagram_api_bp.route('/instagram/hashtags/most-used/recent-ten-posts', methods=['GET'])
def get_instagram_hashtags_most_used_recent_ten():
    try:
        result = main_db.instagram_post_info.aggregate([
            {"$sort": {"date": -1}},
            {"$limit": 1},
            {"$unwind": "$post"},
            {"$limit": 10},
            {"$project": {
                "datetime": "$post.taken_at",
                "hashtags": "$post.hashtags",
                "_id": 0
            }},
            {"$unwind": "$hashtags"},
            {"$sort": {"datetime": -1}},
            {"$group":
                 {"_id": "$hashtags", "count": {"$sum": 1}}
             },
            {"$sort": {"count": -1}},
            {"$limit": 10}
        ])
        return dumps({'result': result})
    except Exception as e:
        return dumps({'err': str(e)})

@instagram_api_bp.route('/instagram/hashtags/most-used/recent-thirty-posts', methods=['GET'])
def get_instagram_hashtags_most_used_recent_thirty():
    try:
        result = main_db.instagram_post_info.aggregate([
            {"$sort": {"date": -1}},
            {"$limit": 1},
            {"$unwind": "$post"},
            {"$limit": 30},
            {"$project": {
                "datetime": "$post.taken_at",
                "hashtags": "$post.hashtags",
                "_id": 0
            }},
            {"$unwind": "$hashtags"},
            {"$sort": {"datetime": -1}},
            {"$group":
                 {"_id": "$hashtags", "count": {"$sum": 1}}
             },
            {"$sort": {"count": -1}},
            {"$limit": 10}
        ])
        return dumps({'result': result})
    except Exception as e:
        return dumps({'err': str(e)})

@instagram_api_bp.route('/instagram/hashtags/most-used/overall-posts', methods=['GET'])
def get_instagram_hashtags_most_used_overall():
    try:
        result = main_db.instagram_post_info.aggregate([
            {"$sort": {"date": -1}},
            {"$limit": 1},
            {"$unwind": "$post"},
            {"$project": {
                "datetime": "$post.taken_at",
                "hashtags": "$post.hashtags",
                "_id": 0
            }},
            {"$unwind": "$hashtags"},
            {"$sort": {"datetime": -1}},
            {"$group":
                 {"_id": "$hashtags", "count": {"$sum": 1}}
             },
            {"$sort": {"count": -1}},
            {"$limit": 10}
        ])
        return dumps({'result': result})
    except Exception as e:
        return dumps({'err': str(e)})

# instagram most-engaged hashtags
@instagram_api_bp.route('/instagram/hashtags/most-engaged/recent-ten-posts', methods=['GET'])
def get_instagram_hashtags_most_engaged_recent_ten():
    try:
        result = main_db.display_instagram_post.aggregate([
            {"$sort": {"datetime": -1}},
            {"$limit": 1},
            {"$unwind": "$data"},
            {"$addFields": {
                "sub_total": {
                    "$sum": ["$data.comment_count", "$data.like_count"]}
            }},
            {"$lookup": {
                "from": "instagram_user_info",
                "localField": "date",
                "foreignField": "datetime",
                "as": "instagram_user_info"
            }},
            {"$project": {
                "_id": 0,
                "post_date": "$datetime",
                "sub_total": "$sub_total",
                "hashtags": "$data.hashtags",
                "follower": {"$slice": ["$instagram_user_info.follower_count", -1]}
            }},
            {"$limit": 10},
            {"$unwind": "$follower"},
            {"$unwind": "$hashtags"},
            {"$addFields": {
                "_eng_rate": {"$divide": ["$sub_total", "$follower"]}
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
                    "$multiply": ["$eng_rate_per_hashtag", 100]
                }
            }},
            {"$sort": {"eng_rate_per_hashtag": -1}},
            {"$limit": 10}
        ])
        return dumps({'result': result})
    except Exception as e:
        return dumps({'err': str(e)})

@instagram_api_bp.route('/instagram/hashtags/most-engaged/recent-thirty-posts', methods=['GET'])
def get_instagram_hashtags_most_engaged_recent_thirty():
    try:
        result = main_db.display_instagram_post.aggregate([
            {"$sort": {"datetime": -1}},
            {"$limit": 1},
            {"$unwind": "$data"},
            {"$addFields": {
                "sub_total": {
                    "$sum": ["$data.comment_count", "$data.like_count"]}
            }},
            {"$lookup": {
                "from": "instagram_user_info",
                "localField": "date",
                "foreignField": "datetime",
                "as": "instagram_user_info"
            }},
            {"$project": {
                "_id": 0,
                "post_date": "$datetime",
                "sub_total": "$sub_total",
                "hashtags": "$data.hashtags",
                "follower": {"$slice": ["$instagram_user_info.follower_count", -1]}
            }},
            {"$limit": 30},
            {"$unwind": "$follower"},
            {"$unwind": "$hashtags"},
            {"$addFields": {
                "_eng_rate": {"$divide": ["$sub_total", "$follower"]}
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
                    "$multiply": ["$eng_rate_per_hashtag", 100]
                }
            }},
            {"$sort": {"eng_rate_per_hashtag": -1}},
            {"$limit": 10}
        ])
        return dumps({'result': result})
    except Exception as e:
        return dumps({'err': str(e)})

@instagram_api_bp.route('/instagram/hashtags/most-engaged/overall-posts', methods=['GET'])
def get_instagram_hashtags_most_engaged_overall():
    try:
        result = main_db.display_instagram_post.aggregate([
            {"$sort": {"datetime": -1}},
            {"$limit": 1},
            {"$unwind": "$data"},
            {"$addFields": {
                "sub_total": {
                    "$sum": ["$data.comment_count", "$data.like_count"]}
            }},
            {"$lookup": {
                "from": "instagram_user_info",
                "localField": "date",
                "foreignField": "datetime",
                "as": "instagram_user_info"
            }},
            {"$project": {
                "_id": 0,
                "post_date": "$datetime",
                "sub_total": "$sub_total",
                "hashtags": "$data.hashtags",
                "follower": {"$slice": ["$instagram_user_info.follower_count", -1]}
            }},
            {"$unwind": "$follower"},
            {"$unwind": "$hashtags"},
            {"$addFields": {
                "_eng_rate": {"$divide": ["$sub_total", "$follower"]}
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
                    "$multiply": ["$eng_rate_per_hashtag", 100]
                }
            }},
            {"$sort": {"eng_rate_per_hashtag": -1}},
            {"$limit": 10}
        ])
        return dumps({'result': result})
    except Exception as e:
        return dumps({'err': str(e)})

class InstagramPost(Resource):
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
        posts_count_cur = main_db.display_instagram_post.aggregate([
            {"$sort": {"datetime": -1}},
            {"$limit": 1},
            {"$unwind": "$data"},
            {"$group": {"_id": "total", "count": {"$sum":1}}}
        ])

        for item in posts_count_cur:
            _temp_list.append(item['count'])

        posts_count = _temp_list[0]

        # Sort By: Date/ Most Likes/ Most Comments
        # case 1: Date
        if (sort == 'date'):
            # fetch all posts
            fetch_posts = main_db.display_instagram_post.aggregate([
                {"$sort": {"datetime": -1}},
                {"$limit": 1},
                {"$unwind": "$data"},
                {"$project": {
                    "_id": 0,
                    "post_date": "$data.post_date",
                    "title": "$data.title",
                    "comment_count": "$data.comment_count",
                    "like_count": "$data.like_count",
                    "hashtags": "$data.hashtags",
                    "image": "$data.new_image_url",
                    "code": "$data.code",
                    "cat": "$data.cat"
                }},
                {"$addFields": {
                    "former_url": "https://instagram.com/p/"
                }},
                {"$project": {
                    "_id": 0,
                    "post_date": "$post_date",
                    "title": "$title",
                    "comment_count": "$comment_count",
                    "like_count": "$like_count",
                    "hashtags": "$hashtags",
                    "image": "$image",
                    "url": {"$concat": ["$former_url", "$code", "/"]},
                    "cat": "$cat"
                }},
                {"$sort": {"post_date": -1}},
                {"$skip": int(page_limit) * (int(page) - 1)},
                {"$limit": int(page_limit)}
            ])

            posts_list = []
            for post in fetch_posts:
                posts_list.append(post)

            response = {'total_posts_count': posts_count, 'page': int(page), 'perPage': int(page_limit), 'sort': sort, 'posts': posts_list}

            return {'result': response}
        elif (sort == 'like'):
            fetch_posts = main_db.display_instagram_post.aggregate([
                {"$sort": {"datetime": -1}},
                {"$limit": 1},
                {"$unwind": "$data"},
                {"$project": {
                    "_id": 0,
                    "post_date": "$data.post_date",
                    "title": "$data.title",
                    "comment_count": "$data.comment_count",
                    "like_count": "$data.like_count",
                    "hashtags": "$data.hashtags",
                    "image": "$data.new_image_url",
                    "code": "$data.code",
                    "cat": "$data.cat"
                }},
                {"$addFields": {
                    "former_url": "https://instagram.com/p/"
                }},
                {"$project": {
                    "_id": 0,
                    "post_date": "$post_date",
                    "title": "$title",
                    "comment_count": "$comment_count",
                    "like_count": "$like_count",
                    "hashtags": "$hashtags",
                    "image": "$image",
                    "url": {"$concat": ["$former_url", "$code", "/"]},
                    "cat": "$cat"
                }},
                {"$sort": {"like_count": -1}},
                {"$skip": int(page_limit) * (int(page) - 1)},
                {"$limit": int(page_limit)}
            ])

            posts_list = []
            for post in fetch_posts:
                posts_list.append(post)

            response = {'total_posts_count': posts_count, 'page': int(page), 'perPage': int(page_limit), 'sort': sort, 'posts': posts_list}

            return {'result': response}

        elif (sort == 'comment'):
            fetch_posts = main_db.display_instagram_post.aggregate([
                {"$sort": {"datetime": -1}},
                {"$limit": 1},
                {"$unwind": "$data"},
                {"$project": {
                    "_id": 0,
                    "post_date": "$data.post_date",
                    "title": "$data.title",
                    "comment_count": "$data.comment_count",
                    "like_count": "$data.like_count",
                    "hashtags": "$data.hashtags",
                    "image": "$data.new_image_url",
                    "code": "$data.code",
                    "cat": "$data.cat"
                }},
                {"$addFields": {
                    "former_url": "https://instagram.com/p/"
                }},
                {"$project": {
                    "_id": 0,
                    "post_date": "$post_date",
                    "title": "$title",
                    "comment_count": "$comment_count",
                    "like_count": "$like_count",
                    "hashtags": "$hashtags",
                    "image": "$image",
                    "url": {"$concat": ["$former_url", "$code", "/"]},
                    "cat": "$cat"
                }},
                {"$sort": {"comment_count": -1}},
                {"$skip": int(page_limit) * (int(page) - 1)},
                {"$limit": int(page_limit)}
            ])

            posts_list = []
            for post in fetch_posts:
                posts_list.append(post)

            response = {'total_posts_count': posts_count, 'page': int(page), 'perPage': int(page_limit), 'sort': sort, 'posts': posts_list}

            return {'result': response}
        elif (sort == 'engaged'):
            fetch_posts = main_db.display_instagram_post.aggregate([
                {"$sort": {"datetime": -1}},
                {"$limit": 1},
                {"$unwind": "$data"},
                {"$addFields": {
                    "sub_total": {
                        "$sum": ["$data.comment_count", "$data.like_count"]}
                }},
                {"$lookup": {
                    "from": "instagram_user_info",
                    "localField": "date",
                    "foreignField": "datetime",
                    "as": "instagram_user_info"
                }},
                {"$project": {
                    "_id": 0,
                    "post_date": "$data.post_date",
                    "title": "$data.title",
                    "comment_count": "$data.comment_count",
                    "like_count": "$data.like_count",
                    "hashtags": "$data.hashtags",
                    "image": "$data.new_image_url",
                    "code": "$data.code",
                    "cat": "$data.cat",
                    "follower": {"$slice": ["$instagram_user_info.follower_count", -1]}
                }},
                {"$addFields": {
                    "former_url": "https://instagram.com/p/"
                }},
                {"$project": {
                    "_id": 0,
                    "post_date": "$post_date",
                    "title": "$title",
                    "comment_count": "$comment_count",
                    "like_count": "$like_count",
                    "hashtags": "$hashtags",
                    "image": "$image",
                    "follower": "$follower",
                    "url": {"$concat": ["$former_url", "$code", "/"]},
                    "cat": "$cat"
                }},
                {"$unwind": "$follower"},
                {"$addFields": {
                    "sub_total": {
                        "$sum": ["$comment_count", "$like_count"]}
                }},
                {"$addFields": {
                    "eng_rate": {"$divide": ["$sub_total", "$follower"]}
                }},
                {"$project": {
                    "post_date": "$post_date",
                    "title": "$title",
                    "comment_count": "$comment_count",
                    "like_count": "$like_count",
                    "hashtags": "$hashtags",
                    "image": "$image",
                    "follower": "$follower",
                    "url": "$url",
                    "eng_rate": {
                        "$multiply": ["$eng_rate", 100]
                    },
                    "cat": "$cat"
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
        else:
            # fetch all posts
            fetch_posts = main_db.display_instagram_post.aggregate([
                {"$sort": {"datetime": -1}},
                {"$limit": 1},
                {"$unwind": "$data"},
                {"$project": {
                    "_id": 0,
                    "post_date": "$data.post_date",
                    "title": "$data.title",
                    "comment_count": "$data.comment_count",
                    "like_count": "$data.like_count",
                    "hashtags": "$data.hashtags",
                    "image": "$data.new_image_url",
                    "code": "$data.code",
                    "cat": "$data.cat"
                }},
                {"$addFields": {
                    "former_url": "https://instagram.com/p/"
                }},
                {"$project": {
                    "_id": 0,
                    "post_date": "$post_date",
                    "title": "$title",
                    "comment_count": "$comment_count",
                    "like_count": "$like_count",
                    "hashtags": "$hashtags",
                    "image": "$image",
                    "url": {"$concat": ["$former_url", "$code", "/"]},
                    "cat": "$cat"
                }},
                {"$sort": {"post_date": -1}},
                {"$skip": int(page_limit) * (int(page) - 1)},
                {"$limit": int(page_limit)}
            ])

            posts_list = []
            for post in fetch_posts:
                posts_list.append(post)

            response = {'total_posts_count': posts_count, 'page': int(page), 'perPage': int(page_limit), 'sort': sort, 'posts': posts_list}

            return {'result': response}