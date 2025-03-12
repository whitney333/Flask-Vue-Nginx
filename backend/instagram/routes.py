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
        result = main_db.instagram_post_info.aggregate([
            {"$sort": {"datetime": -1}},
            {"$limit": 1},
            {"$unwind": "$post"},
            {"$addFields": {
                "sub_total": {
                    "$sum": ["$post.comment_count", "$post.like_count"]}
            }},
            {"$project": {
                "_id": 0,
                "post_date": "$datetime",
                "sub_total": "$sub_total",
                "hashtags": "$post.hashtags",
                "follower": "$follower_count"
            }},
            {"$limit": 10},
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
        result = main_db.instagram_post_info.aggregate([
            {"$sort": {"datetime": -1}},
            {"$limit": 1},
            {"$unwind": "$post"},
            {"$addFields": {
                "sub_total": {
                    "$sum": ["$post.comment_count", "$post.like_count"]}
            }},
            {"$project": {
                "_id": 0,
                "post_date": "$datetime",
                "sub_total": "$sub_total",
                "hashtags": "$post.hashtags",
                "follower": "$follower_count"
            }},
            {"$limit": 30},
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
        result = main_db.instagram_post_info.aggregate([
            {"$sort": {"datetime": -1}},
            {"$limit": 1},
            {"$unwind": "$post"},
            {"$addFields": {
                "sub_total": {
                    "$sum": ["$post.comment_count", "$post.like_count"]}
            }},
            {"$project": {
                "_id": 0,
                "post_date": "$datetime",
                "sub_total": "$sub_total",
                "hashtags": "$post.hashtags",
                "follower": "$follower_count"
            }},
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

@instagram_api_bp.route('/instagram/posts', methods=['GET'])
def get_instagram_post():
    try:
        results = main_db.instagram_post_info.aggregate([
            {"$sort": {"date": -1}},
            {"$limit": 1},
            {"$project": {
                "_id": 0,
                "date": {
                    "$dateToString": {
                        "format": "%Y-%m-%d",
                        "date": "$date"
                    }
                },
                "media_count": "$media_count",
                "follower_count": "$follower_count",
                "posts": "$post"
            }},
            {"$unwind": "$posts"},
            {"$addFields": {
                "eng_rate": {
                    "$round": [{
                        "$multiply": [
                            {"$divide": [
                                {"$sum": ["$posts.comment_count", "$posts.like_count"]}, "$follower_count"
                            ]}, 100
                        ]
                    }, 3]
                }
            }},
            # return frontend fields
            {"$project": {
                "_id": "$posts.id",
                "datetime": "$date",
                "media_count": "$media_count",
                "follower_count": "$follower_count",
                "username": "$posts.username",
                "upload_date": "$posts.taken_at",
                "media_type": "$posts.media_type",
                "product_type": "$posts.product_type",
                "user_pk": "$posts.user.pk",
                "comment_count": "$posts.comment_count",
                "like_count": "$posts.like_count",
                "caption_text": "$posts.caption_text",
                "music_id": "$posts.music_canonical_id",
                "hashtags": "$posts.hashtags",
                "cat": "$posts.cat",
                "thumbnail": "$posts.thumbnail_url",
                "eng_rate": "$eng_rate",
                "url": {"$concat": ["https://instagram.com/p/", "$posts.code", "/"]}
            }},
            # calculate eng rate, and round to 2 decimal points
            # add post url
            {"$sort": {"upload_date": -1}}
        ])
        return dumps({'result': results})
    except Exception as e:
        return dumps({'error': str(e)})

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
        posts_count_cur = main_db.instagram_post_info.aggregate([
            {"$sort": {"date": -1}},
            {"$limit": 1},
            {"$unwind": "$post"},
            {"$group": {"_id": "total", "count": {"$sum":1}}}
        ])

        for item in posts_count_cur:
            _temp_list.append(item['count'])

        posts_count = _temp_list[0]

        # Sort By: Date/ Most Likes/ Most Comments
        # case 1: Date
        if (sort == 'date'):
            # fetch all posts
            fetch_posts = main_db.instagram_post_info.aggregate([
                {"$sort": {"date": -1}},
                {"$limit": 1},
                {"$unwind": "$post"},
                {"$project": {
                    "_id": 0,
                    "post_date": "$post.taken_at",
                    "title": "$post.caption_text",
                    "comment_count": "$post.comment_count",
                    "like_count": "$post.like_count",
                    "hashtags": "$post.hashtags",
                    "image": "$post.thumbnail_url",
                    "code": "$post.code",
                    "cat": "$post.cat"
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
                    "image": {"$split": ["$image", "/"]},
                    "url": {"$concat": ["$former_url", "$code", "/"]},
                    "cat": "$cat"
                }},
                {"$match": {
                    "image.2": {"$exists": 1}
                }},
                {"$project": {
                    "_id": 0,
                    "title": "$title",
                    "post_date": "$post_date",
                    "comment_count": "$comment_count",
                    "like_count": "$like_count",
                    "hashtags": "$hashtags",
                    "url": "$url",
                    "cat": "$cat",
                    "image": {"$arrayElemAt": ["$image", 5]}
                }},
                {"$project": {
                    "_id": 0,
                    "title": "$title",
                    "post_date": "$post_date",
                    "comment_count": "$comment_count",
                    "like_count": "$like_count",
                    "hashtags": "$hashtags",
                    "url": "$url",
                    "cat": "$cat",
                    "image": {"$split": ["$image", "?"]}
                }},
                {"$match": {
                    "image.1": {"$exists": 1}
                }},
                {"$project": {
                    "_id": 0,
                    "title": "$title",
                    "post_date": "$post_date",
                    "comment_count": "$comment_count",
                    "like_count": "$like_count",
                    "hashtags": "$hashtags",
                    "url": "$url",
                    "cat": "$cat",
                    "image": {"$arrayElemAt": ["$image", 0]}
                }},
                {"$addFields": {
                    "former_img_url": "https://mishkan-ltd.s3.ap-northeast-2.amazonaws.com/web-x/instagram-post-cover/"
                }},
                {"$project": {
                    "_id": 0,
                    "title": "$title",
                    "post_date": {
                        "$dateToString": {
                            "format": "%Y-%m-%d",
                            "date": "$post_date"
                        }
                    },
                    "comment_count": "$comment_count",
                    "like_count": "$like_count",
                    "hashtags": "$hashtags",
                    "url": "$url",
                    "cat": "$cat",
                    "image": {"$concat": ["$former_img_url", "$image"]}
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
            fetch_posts = main_db.instagram_post_info.aggregate([
                {"$sort": {"date": -1}},
                {"$limit": 1},
                {"$unwind": "$post"},
                {"$project": {
                    "_id": 0,
                    "post_date": "$post.taken_at",
                    "title": "$post.caption_text",
                    "comment_count": "$post.comment_count",
                    "like_count": "$post.like_count",
                    "hashtags": "$post.hashtags",
                    "image": "$post.thumbnail_url",
                    "code": "$post.code",
                    "cat": "$post.cat"
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
                    "image": {"$split": ["$image", "/"]},
                    "url": {"$concat": ["$former_url", "$code", "/"]},
                    "cat": "$cat"
                }},
                {"$match": {
                    "image.2": {"$exists": 1}
                }},
                {"$project": {
                    "_id": 0,
                    "title": "$title",
                    "post_date": "$post_date",
                    "comment_count": "$comment_count",
                    "like_count": "$like_count",
                    "hashtags": "$hashtags",
                    "url": "$url",
                    "cat": "$cat",
                    "image": {"$arrayElemAt": ["$image", 5]}
                }},
                {"$project": {
                    "_id": 0,
                    "title": "$title",
                    "post_date": "$post_date",
                    "comment_count": "$comment_count",
                    "like_count": "$like_count",
                    "hashtags": "$hashtags",
                    "url": "$url",
                    "cat": "$cat",
                    "image": {"$split": ["$image", "?"]}
                }},
                {"$match": {
                    "image.1": {"$exists": 1}
                }},
                {"$project": {
                    "_id": 0,
                    "title": "$title",
                    "post_date": "$post_date",
                    "comment_count": "$comment_count",
                    "like_count": "$like_count",
                    "hashtags": "$hashtags",
                    "url": "$url",
                    "cat": "$cat",
                    "image": {"$arrayElemAt": ["$image", 0]}
                }},
                {"$addFields": {
                    "former_img_url": "https://mishkan-ltd.s3.ap-northeast-2.amazonaws.com/web-x/instagram-post-cover/"
                }},
                {"$project": {
                    "_id": 0,
                    "title": "$title",
                    "post_date": {
                        "$dateToString": {
                            "format": "%Y-%m-%d",
                            "date": "$post_date"
                        }
                    },
                    "comment_count": "$comment_count",
                    "like_count": "$like_count",
                    "hashtags": "$hashtags",
                    "url": "$url",
                    "cat": "$cat",
                    "image": {"$concat": ["$former_img_url", "$image"]}
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
            fetch_posts = main_db.instagram_post_info.aggregate([
                {"$sort": {"date": -1}},
                {"$limit": 1},
                {"$unwind": "$post"},
                {"$project": {
                    "_id": 0,
                    "post_date": "$post.taken_at",
                    "title": "$post.caption_text",
                    "comment_count": "$post.comment_count",
                    "like_count": "$post.like_count",
                    "hashtags": "$post.hashtags",
                    "image": "$post.thumbnail_url",
                    "code": "$post.code",
                    "cat": "$post.cat"
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
                    "image": {"$split": ["$image", "/"]},
                    "url": {"$concat": ["$former_url", "$code", "/"]},
                    "cat": "$cat"
                }},
                {"$match": {
                    "image.2": {"$exists": 1}
                }},
                {"$project": {
                    "_id": 0,
                    "title": "$title",
                    "post_date": "$post_date",
                    "comment_count": "$comment_count",
                    "like_count": "$like_count",
                    "hashtags": "$hashtags",
                    "url": "$url",
                    "cat": "$cat",
                    "image": {"$arrayElemAt": ["$image", 5]}
                }},
                {"$project": {
                    "_id": 0,
                    "title": "$title",
                    "post_date": "$post_date",
                    "comment_count": "$comment_count",
                    "like_count": "$like_count",
                    "hashtags": "$hashtags",
                    "url": "$url",
                    "cat": "$cat",
                    "image": {"$split": ["$image", "?"]}
                }},
                {"$match": {
                    "image.1": {"$exists": 1}
                }},
                {"$project": {
                    "_id": 0,
                    "title": "$title",
                    "post_date": "$post_date",
                    "comment_count": "$comment_count",
                    "like_count": "$like_count",
                    "hashtags": "$hashtags",
                    "url": "$url",
                    "cat": "$cat",
                    "image": {"$arrayElemAt": ["$image", 0]}
                }},
                {"$addFields": {
                    "former_img_url": "https://mishkan-ltd.s3.ap-northeast-2.amazonaws.com/web-x/instagram-post-cover/"
                }},
                {"$project": {
                    "_id": 0,
                    "title": "$title",
                    "post_date": {
                        "$dateToString": {
                            "format": "%Y-%m-%d",
                            "date": "$post_date"
                        }
                    },
                    "comment_count": "$comment_count",
                    "like_count": "$like_count",
                    "hashtags": "$hashtags",
                    "url": "$url",
                    "cat": "$cat",
                    "image": {"$concat": ["$former_img_url", "$image"]}
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
            fetch_posts = main_db.instagram_post_info.aggregate([
                {"$sort": {"date": -1}},
                {"$limit": 1},
                {"$unwind": "$post"},
                {"$lookup": {
                    "from": "instagram_user_info",
                    "localField": "date",
                    "foreignField": "date",
                    "as": "instagram_user_info"
                }},
                {"$project": {
                    "_id": 0,
                    "date": "$date",
                    "post_date": "$post.taken_at",
                    "title": "$post.caption_text",
                    "comment_count": "$post.comment_count",
                    "like_count": "$post.like_count",
                    "hashtags": "$post.hashtags",
                    "image": "$post.thumbnail_url",
                    "code": "$post.code",
                    "cat": "$post.cat",
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
                    "image": {"$split": ["$image", "/"]},
                    "url": {"$concat": ["$former_url", "$code", "/"]},
                    "cat": "$cat",
                    "follower": "$follower",
                }},
                {"$addFields": {
                    "sub_total": {
                        "$sum": ["$comment_count", "$like_count"]}
                }},
                {"$unwind": "$follower"},
                {"$addFields": {
                    "eng_rate": {"$divide": ["$sub_total", "$follower"]}
                }},
                {"$match": {
                    "image.2": {"$exists": 1}
                }},
                {"$project": {
                    "_id": 0,
                    "title": "$title",
                    "post_date": "$post_date",
                    "comment_count": "$comment_count",
                    "like_count": "$like_count",
                    "hashtags": "$hashtags",
                    "url": "$url",
                    "cat": "$cat",
                    "sub_total": "$sub_total",
                    "follower": "$follower",
                    "eng_rate": "$eng_rate",
                    "image": {"$arrayElemAt": ["$image", 5]}
                }},
                {"$project": {
                    "_id": 0,
                    "title": "$title",
                    "post_date": "$post_date",
                    "comment_count": "$comment_count",
                    "like_count": "$like_count",
                    "hashtags": "$hashtags",
                    "url": "$url",
                    "cat": "$cat",
                    "sub_total": "$sub_total",
                    "follower": "$follower",
                    "eng_rate": "$eng_rate",
                    "image": {"$split": ["$image", "?"]}
                }},
                {"$match": {
                    "image.1": {"$exists": 1}
                }},
                {"$project": {
                    "_id": 0,
                    "post_date": "$post_date",
                    "title": "$title",
                    "comment_count": "$comment_count",
                    "like_count": "$like_count",
                    "hashtags": "$hashtags",
                    "url": "$url",
                    "cat": "$cat",
                    "sub_total": "$sub_total",
                    "follower": "$follower",
                    "eng_rate": "$eng_rate",
                    "image": {"$arrayElemAt": ["$image", 0]}
                }},
                {"$addFields": {
                    "former_img_url": "https://mishkan-ltd.s3.ap-northeast-2.amazonaws.com/web-x/instagram-post-cover/"
                }},
                {"$project": {
                    "_id": 0,
                    "post_date": {
                        "$dateToString": {
                            "format": "%Y-%m-%d",
                            "date": "$post_date"
                        }
                    },
                    "title": "$title",
                    "comment_count": "$comment_count",
                    "like_count": "$like_count",
                    "hashtags": "$hashtags",
                    "url": "$url",
                    "cat": "$cat",
                    "eng_rate": {
                        "$multiply": ["$eng_rate", 100]
                    },
                    "image": {"$concat": ["$former_img_url", "$image"]}
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
            fetch_posts = main_db.instagram_post_info.aggregate([
                {"$sort": {"date": -1}},
                {"$limit": 1},
                {"$unwind": "$post"},
                {"$project": {
                    "_id": 0,
                    "post_date": "$post.taken_at",
                    "title": "$post.caption_text",
                    "comment_count": "$post.comment_count",
                    "like_count": "$post.like_count",
                    "hashtags": "$post.hashtags",
                    "image": "$post.thumbnail_url",
                    "code": "$post.code",
                    "cat": "$post.cat"
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
                    "image": {"$split": ["$image", "/"]},
                    "url": {"$concat": ["$former_url", "$code", "/"]},
                    "cat": "$cat"
                }},
                {"$match": {
                    "image.2": {"$exists": 1}
                }},
                {"$project": {
                    "_id": 0,
                    "title": "$title",
                    "post_date": "$post_date",
                    "comment_count": "$comment_count",
                    "like_count": "$like_count",
                    "hashtags": "$hashtags",
                    "url": "$url",
                    "cat": "$cat",
                    "image": {"$arrayElemAt": ["$image", 5]}
                }},
                {"$project": {
                    "_id": 0,
                    "title": "$title",
                    "post_date": "$post_date",
                    "comment_count": "$comment_count",
                    "like_count": "$like_count",
                    "hashtags": "$hashtags",
                    "url": "$url",
                    "cat": "$cat",
                    "image": {"$split": ["$image", "?"]}
                }},
                {"$match": {
                    "image.1": {"$exists": 1}
                }},
                {"$project": {
                    "_id": 0,
                    "title": "$title",
                    "post_date": "$post_date",
                    "comment_count": "$comment_count",
                    "like_count": "$like_count",
                    "hashtags": "$hashtags",
                    "url": "$url",
                    "cat": "$cat",
                    "image": {"$arrayElemAt": ["$image", 0]}
                }},
                {"$addFields": {
                    "former_img_url": "https://mishkan-ltd.s3.ap-northeast-2.amazonaws.com/web-x/instagram-post-cover/"
                }},
                {"$project": {
                    "_id": 0,
                    "title": "$title",
                    "post_date": {
                        "$dateToString": {
                            "format": "%Y-%m-%d",
                            "date": "$post_date"
                        }
                    },
                    "comment_count": "$comment_count",
                    "like_count": "$like_count",
                    "hashtags": "$hashtags",
                    "url": "$url",
                    "cat": "$cat",
                    "image": {"$concat": ["$former_img_url", "$image"]}
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


class InstagramPostCategory(Resource):
    def get(self):
        posts_data = reqparse.RequestParser()
        posts_data.add_argument('cat', type=int, required=True, help='Limit number is required', location='args')
        data = posts_data.parse_args()

        cat = data['cat']
        _temp_list = []

        # fetch post categories and calculate their engagement rate
        # params: latest 10 posts/ 30 posts/ all posts
        if (cat == 10):
            fetch_posts = main_db.instagram_post_info.aggregate([
                {"$sort": {"date": -1}},
                {"$limit": 1},
                {"$unwind": "$post"},
                {"$addFields": {
                    "sub_total": {
                        "$sum": ["$post.comment_count", "$post.like_count"]}
                }},
                {"$project": {
                    "date": "$date",
                    "media_count": "$media_count",
                    "follower_count": "$follower_count",
                    "sub_total": "$sub_total",
                    "pk": "$post.pk",
                    "id": "$post.id",
                    "code": "$post.code",
                    "taken_at": "$post.taken_at",
                    "media_type": "$post.media_type",
                    "product_type": "$post.product_type",
                    "thumbnail_url": "$post.thumbnail_url",
                    "location": "$post.location",
                    "user": "$post.user",
                    "comment_count": "$post.comment_count",
                    "like_count": "$post.like_count",
                    "has_liked": "$post.has_Liked",
                    "caption_text": "$post.caption_text",
                    "accessibility_caption": "$post.accessibility_caption",
                    "usertags": "$post.usertags",
                    "video_url": "$post.video_url",
                    "view_count": "$post.view_count",
                    "video_duration": "$post.video_duration",
                    "title": "$post.title",
                    "resources": "$post.resources",
                    "clips_metadata": "$post.clips_metadata",
                    "username": "$post.username",
                    "hashtags": "$post.hashtags",
                    "cat": "$post.cat",
                }},
                {"$addFields": {
                    "_eng_rate": {"$divide": ["$sub_total", "$follower_count"]}
                }},
                {"$sort": {"taken_at": -1}},
                {"$limit": 10},
                {"$unwind": "$cat"},
                {"$group": {
                    "_id": "$cat",
                    "count": {"$sum": {"$toInt": 1}},
                    "_total_eng_rate": {"$sum": "$_eng_rate"},
                }},
                {"$project": {
                    "eng_rate_by_cat": {
                        "$divide": ["$_total_eng_rate", "$count"]
                    }
                }},
                {"$project": {
                    "eng_rate_by_cat": {
                        "$round": [
                            {"$multiply": ["$eng_rate_by_cat", 100]}, 2
                    ]}
                }},
                {"$sort": {"eng_rate_by_cat": -1}},
                {"$limit": 10}
            ])

            posts_list = []
            for post in fetch_posts:
                posts_list.append(post)

            response = {'cat': posts_list}

            return {'result': response}
        elif (cat == 30):
            fetch_posts = main_db.instagram_post_info.aggregate([
                {"$sort": {"date": -1}},
                {"$limit": 1},
                {"$unwind": "$post"},
                {"$addFields": {
                    "sub_total": {
                        "$sum": ["$post.comment_count", "$post.like_count"]}
                }},
                {"$project": {
                    "date": "$date",
                    "media_count": "$media_count",
                    "follower_count": "$follower_count",
                    "sub_total": "$sub_total",
                    "pk": "$post.pk",
                    "id": "$post.id",
                    "code": "$post.code",
                    "taken_at": "$post.taken_at",
                    "media_type": "$post.media_type",
                    "product_type": "$post.product_type",
                    "thumbnail_url": "$post.thumbnail_url",
                    "location": "$post.location",
                    "user": "$post.user",
                    "comment_count": "$post.comment_count",
                    "like_count": "$post.like_count",
                    "has_liked": "$post.has_Liked",
                    "caption_text": "$post.caption_text",
                    "accessibility_caption": "$post.accessibility_caption",
                    "usertags": "$post.usertags",
                    "video_url": "$post.video_url",
                    "view_count": "$post.view_count",
                    "video_duration": "$post.video_duration",
                    "title": "$post.title",
                    "resources": "$post.resources",
                    "clips_metadata": "$post.clips_metadata",
                    "username": "$post.username",
                    "hashtags": "$post.hashtags",
                    "cat": "$post.cat",
                }},
                {"$addFields": {
                    "_eng_rate": {"$divide": ["$sub_total", "$follower_count"]}
                }},
                {"$sort": {"taken_at": -1}},
                {"$limit": 30},
                {"$unwind": "$cat"},
                {"$group": {
                    "_id": "$cat",
                    "count": {"$sum": {"$toInt": 1}},
                    "_total_eng_rate": {"$sum": "$_eng_rate"},
                }},
                {"$project": {
                    "eng_rate_by_cat": {
                        "$divide": ["$_total_eng_rate", "$count"]
                    }
                }},
                {"$project": {
                    "eng_rate_by_cat": {
                        "$round": [
                            {"$multiply": ["$eng_rate_by_cat", 100]}, 2
                        ]}
                }},
                {"$sort": {"eng_rate_by_cat": -1}},
                {"$limit": 10}
            ])

            posts_list = []
            for post in fetch_posts:
                posts_list.append(post)

            response = {'cat': posts_list}

            return {'result': response}
        elif (cat == 0):
            fetch_posts = main_db.instagram_post_info.aggregate([
                {"$sort": {"date": -1}},
                {"$limit": 1},
                {"$unwind": "$post"},
                {"$addFields": {
                    "sub_total": {
                        "$sum": ["$post.comment_count", "$post.like_count"]}
                }},
                {"$project": {
                    "date": "$date",
                    "media_count": "$media_count",
                    "follower_count": "$follower_count",
                    "sub_total": "$sub_total",
                    "pk": "$post.pk",
                    "id": "$post.id",
                    "code": "$post.code",
                    "taken_at": "$post.taken_at",
                    "media_type": "$post.media_type",
                    "product_type": "$post.product_type",
                    "thumbnail_url": "$post.thumbnail_url",
                    "location": "$post.location",
                    "user": "$post.user",
                    "comment_count": "$post.comment_count",
                    "like_count": "$post.like_count",
                    "has_liked": "$post.has_Liked",
                    "caption_text": "$post.caption_text",
                    "accessibility_caption": "$post.accessibility_caption",
                    "usertags": "$post.usertags",
                    "video_url": "$post.video_url",
                    "view_count": "$post.view_count",
                    "video_duration": "$post.video_duration",
                    "title": "$post.title",
                    "resources": "$post.resources",
                    "clips_metadata": "$post.clips_metadata",
                    "username": "$post.username",
                    "hashtags": "$post.hashtags",
                    "cat": "$post.cat",
                }},
                {"$addFields": {
                    "_eng_rate": {"$divide": ["$sub_total", "$follower_count"]}
                }},
                {"$sort": {"taken_at": -1}},
                {"$unwind": "$cat"},
                {"$group": {
                    "_id": "$cat",
                    "count": {"$sum": {"$toInt": 1}},
                    "_total_eng_rate": {"$sum": "$_eng_rate"},
                }},
                {"$project": {
                    "eng_rate_by_cat": {
                        "$divide": ["$_total_eng_rate", "$count"]
                    }
                }},
                {"$project": {
                    "eng_rate_by_cat": {
                        "$round": [
                            {"$multiply": ["$eng_rate_by_cat", 100]}, 2
                        ]}
                }},
                {"$sort": {"eng_rate_by_cat": -1}},
                {"$limit": 10}
            ])

            posts_list = []
            for post in fetch_posts:
                posts_list.append(post)

            response = {'cat': posts_list}

            return {'result': response}
        else:
            fetch_posts = main_db.instagram_post_info.aggregate([
                {"$sort": {"date": -1}},
                {"$limit": 1},
                {"$unwind": "$post"},
                {"$addFields": {
                    "sub_total": {
                        "$sum": ["$post.comment_count", "$post.like_count"]}
                }},
                {"$project": {
                    "date": "$date",
                    "media_count": "$media_count",
                    "follower_count": "$follower_count",
                    "sub_total": "$sub_total",
                    "pk": "$post.pk",
                    "id": "$post.id",
                    "code": "$post.code",
                    "taken_at": "$post.taken_at",
                    "media_type": "$post.media_type",
                    "product_type": "$post.product_type",
                    "thumbnail_url": "$post.thumbnail_url",
                    "location": "$post.location",
                    "user": "$post.user",
                    "comment_count": "$post.comment_count",
                    "like_count": "$post.like_count",
                    "has_liked": "$post.has_Liked",
                    "caption_text": "$post.caption_text",
                    "accessibility_caption": "$post.accessibility_caption",
                    "usertags": "$post.usertags",
                    "video_url": "$post.video_url",
                    "view_count": "$post.view_count",
                    "video_duration": "$post.video_duration",
                    "title": "$post.title",
                    "resources": "$post.resources",
                    "clips_metadata": "$post.clips_metadata",
                    "username": "$post.username",
                    "hashtags": "$post.hashtags",
                    "cat": "$post.cat",
                }},
                {"$addFields": {
                    "_eng_rate": {"$divide": ["$sub_total", "$follower_count"]}
                }},
                {"$sort": {"taken_at": -1}},
                {"$limit": 10},
                {"$unwind": "$cat"},
                {"$group": {
                    "_id": "$cat",
                    "count": {"$sum": {"$toInt": 1}},
                    "_total_eng_rate": {"$sum": "$_eng_rate"},
                }},
                {"$project": {
                    "eng_rate_by_cat": {
                        "$divide": ["$_total_eng_rate", "$count"]
                    }
                }},
                {"$project": {
                    "eng_rate_by_cat": {
                        "$round": [
                            {"$multiply": ["$eng_rate_by_cat", 100]}, 2
                        ]}
                }},
                {"$sort": {"eng_rate_by_cat": -1}},
                {"$limit": 10}
            ])

            posts_list = []
            for post in fetch_posts:
                posts_list.append(post)

            response = {'cat': posts_list}

            return {'result': response}

class InstagramCategoryPercentage(Resource):
    def get(self):
        posts_data = reqparse.RequestParser()
        posts_data.add_argument('post', type=int, required=True, help='Page number is required', location='args')
        data = posts_data.parse_args()

        post = data['post']
        _temp_list = []

        # fetch post categories and calculate their occurrences
        # params: latest 12 posts/ 30 posts/ all posts
        if (post == 12):
            fetch_posts = main_db.instagram_post_info.aggregate([
                {"$sort": {"date": -1}},
                {"$limit": 1},
                {"$unwind": "$post"},
                {"$addFields": {
                    "sub_total": {
                        "$sum": ["$post.comment_count", "$post.like_count"]}
                }},
                {"$project": {
                    "date": "$date",
                    "media_count": "$media_count",
                    "follower_count": "$follower_count",
                    "sub_total": "$sub_total",
                    "pk": "$post.pk",
                    "id": "$post.id",
                    "code": "$post.code",
                    "taken_at": "$post.taken_at",
                    "media_type": "$post.media_type",
                    "product_type": "$post.product_type",
                    "thumbnail_url": "$post.thumbnail_url",
                    "location": "$post.location",
                    "user": "$post.user",
                    "comment_count": "$post.comment_count",
                    "like_count": "$post.like_count",
                    "has_liked": "$post.has_Liked",
                    "caption_text": "$post.caption_text",
                    "accessibility_caption": "$post.accessibility_caption",
                    "usertags": "$post.usertags",
                    "video_url": "$post.video_url",
                    "view_count": "$post.view_count",
                    "video_duration": "$post.video_duration",
                    "title": "$post.title",
                    "resources": "$post.resources",
                    "clips_metadata": "$post.clips_metadata",
                    "username": "$post.username",
                    "hashtags": "$post.hashtags",
                    "cat": "$post.cat"
                }},
                {"$addFields": {
                    "_eng_rate": {"$divide": ["$sub_total", "$follower_count"]}
                }},
                {"$sort": {"taken_at": -1}},
                {"$limit": post},
                {"$unwind": "$cat"},
                {"$group": {
                    "_id": "$id",
                    "cat": {"$first": "$cat"}
                }},
                {"$facet": {
                    "nDocs": [{
                        "$count": "nDocs"
                    }],
                    "groupValues": [
                        {"$group": {
                            "_id": "$cat",
                            "total": {
                                "$sum": {"$toInt": 1}
                            }
                        }
                    }]
                }},
                {"$addFields": {
                    "nDocs": {
                        "$arrayElemAt": [
                            "$nDocs",
                            0
                        ]
                    }
                }},
                {"$unwind": "$groupValues"},
                {"$project": {
                    "_id": 0,
                    "category": "$groupValues._id",
                    "total": "$groupValues.total",
                    "percentage": {
                        "$round": [{
                        "$multiply": [
                            {"$divide": [
                                "$groupValues.total",
                                "$nDocs.nDocs"
                            ]}, 100
                        ]}, 2]
                    }
                }},
                {"$sort": {"percentage": -1}}
            ])
            posts_list = []
            for post in fetch_posts:
                posts_list.append(post)

            response = {'posts': posts_list}

            return {'result': response}
        elif (post == 30):
            fetch_posts = main_db.instagram_post_info.aggregate([
                {"$sort": {"date": -1}},
                {"$limit": 1},
                {"$unwind": "$post"},
                {"$addFields": {
                    "sub_total": {
                        "$sum": ["$post.comment_count", "$post.like_count"]}
                }},
                {"$project": {
                    "date": "$date",
                    "media_count": "$media_count",
                    "follower_count": "$follower_count",
                    "sub_total": "$sub_total",
                    "pk": "$post.pk",
                    "id": "$post.id",
                    "code": "$post.code",
                    "taken_at": "$post.taken_at",
                    "media_type": "$post.media_type",
                    "product_type": "$post.product_type",
                    "thumbnail_url": "$post.thumbnail_url",
                    "location": "$post.location",
                    "user": "$post.user",
                    "comment_count": "$post.comment_count",
                    "like_count": "$post.like_count",
                    "has_liked": "$post.has_Liked",
                    "caption_text": "$post.caption_text",
                    "accessibility_caption": "$post.accessibility_caption",
                    "usertags": "$post.usertags",
                    "video_url": "$post.video_url",
                    "view_count": "$post.view_count",
                    "video_duration": "$post.video_duration",
                    "title": "$post.title",
                    "resources": "$post.resources",
                    "clips_metadata": "$post.clips_metadata",
                    "username": "$post.username",
                    "hashtags": "$post.hashtags",
                    "cat": "$post.cat"
                }},
                {"$addFields": {
                    "_eng_rate": {"$divide": ["$sub_total", "$follower_count"]}
                }},
                {"$sort": {"taken_at": -1}},
                {"$limit": post},
                {"$unwind": "$cat"},
                {"$group": {
                    "_id": "$id",
                    "cat": {"$first": "$cat"}
                }},
                {"$facet": {
                    "nDocs": [{
                        "$count": "nDocs"
                    }],
                    "groupValues": [
                        {"$group": {
                            "_id": "$cat",
                            "total": {
                                "$sum": {"$toInt": 1}
                            }
                        }
                    }]
                }},
                {"$addFields": {
                    "nDocs": {
                        "$arrayElemAt": [
                            "$nDocs",
                            0
                        ]
                    }
                }},
                {"$unwind": "$groupValues"},
                {"$project": {
                    "_id": 0,
                    "category": "$groupValues._id",
                    "total": "$groupValues.total",
                    "percentage": {
                        "$round": [{
                        "$multiply": [
                            {"$divide": [
                                "$groupValues.total",
                                "$nDocs.nDocs"
                            ]}, 100
                        ]}, 2]
                    }
                }},
                {"$sort": {"percentage": -1}}
            ])
            posts_list = []
            for post in fetch_posts:
                posts_list.append(post)

            response = {'posts': posts_list}

            return {'result': response}
        elif (post == 0):
            fetch_posts = main_db.instagram_post_info.aggregate([
                {"$sort": {"date": -1}},
                {"$limit": 1},
                {"$unwind": "$post"},
                {"$addFields": {
                    "sub_total": {
                        "$sum": ["$post.comment_count", "$post.like_count"]}
                }},
                {"$project": {
                    "date": "$date",
                    "media_count": "$media_count",
                    "follower_count": "$follower_count",
                    "sub_total": "$sub_total",
                    "pk": "$post.pk",
                    "id": "$post.id",
                    "code": "$post.code",
                    "taken_at": "$post.taken_at",
                    "media_type": "$post.media_type",
                    "product_type": "$post.product_type",
                    "thumbnail_url": "$post.thumbnail_url",
                    "location": "$post.location",
                    "user": "$post.user",
                    "comment_count": "$post.comment_count",
                    "like_count": "$post.like_count",
                    "has_liked": "$post.has_Liked",
                    "caption_text": "$post.caption_text",
                    "accessibility_caption": "$post.accessibility_caption",
                    "usertags": "$post.usertags",
                    "video_url": "$post.video_url",
                    "view_count": "$post.view_count",
                    "video_duration": "$post.video_duration",
                    "title": "$post.title",
                    "resources": "$post.resources",
                    "clips_metadata": "$post.clips_metadata",
                    "username": "$post.username",
                    "hashtags": "$post.hashtags",
                    "cat": "$post.cat"
                }},
                {"$addFields": {
                    "_eng_rate": {"$divide": ["$sub_total", "$follower_count"]}
                }},
                {"$sort": {"taken_at": -1}},
                {"$unwind": "$cat"},
                {"$group": {
                    "_id": "$id",
                    "cat": {"$first": "$cat"}
                }},
                {"$facet": {
                    "nDocs": [{
                        "$count": "nDocs"
                    }],
                    "groupValues": [
                        {"$group": {
                            "_id": "$cat",
                            "total": {
                                "$sum": {"$toInt": 1}
                            }
                        }
                    }]
                }},
                {"$addFields": {
                    "nDocs": {
                        "$arrayElemAt": [
                            "$nDocs",
                            0
                        ]
                    }
                }},
                {"$unwind": "$groupValues"},
                {"$project": {
                    "_id": 0,
                    "category": "$groupValues._id",
                    "total": "$groupValues.total",
                    "percentage": {
                        "$round": [{
                        "$multiply": [
                            {"$divide": [
                                "$groupValues.total",
                                "$nDocs.nDocs"
                            ]}, 100
                        ]}, 2]
                    }
                }},
                {"$sort": {"percentage": -1}}
            ])
            posts_list = []
            for post in fetch_posts:
                posts_list.append(post)

            response = {'posts': posts_list}

            return {'result': response}
        else:
            fetch_posts = main_db.instagram_post_info.aggregate([
                {"$sort": {"date": -1}},
                {"$limit": 1},
                {"$unwind": "$post"},
                {"$addFields": {
                    "sub_total": {
                        "$sum": ["$post.comment_count", "$post.like_count"]}
                }},
                {"$project": {
                    "date": "$date",
                    "media_count": "$media_count",
                    "follower_count": "$follower_count",
                    "sub_total": "$sub_total",
                    "pk": "$post.pk",
                    "id": "$post.id",
                    "code": "$post.code",
                    "taken_at": "$post.taken_at",
                    "media_type": "$post.media_type",
                    "product_type": "$post.product_type",
                    "thumbnail_url": "$post.thumbnail_url",
                    "location": "$post.location",
                    "user": "$post.user",
                    "comment_count": "$post.comment_count",
                    "like_count": "$post.like_count",
                    "has_liked": "$post.has_Liked",
                    "caption_text": "$post.caption_text",
                    "accessibility_caption": "$post.accessibility_caption",
                    "usertags": "$post.usertags",
                    "video_url": "$post.video_url",
                    "view_count": "$post.view_count",
                    "video_duration": "$post.video_duration",
                    "title": "$post.title",
                    "resources": "$post.resources",
                    "clips_metadata": "$post.clips_metadata",
                    "username": "$post.username",
                    "hashtags": "$post.hashtags",
                    "cat": "$post.cat"
                }},
                {"$addFields": {
                    "_eng_rate": {"$divide": ["$sub_total", "$follower_count"]}
                }},
                {"$sort": {"taken_at": -1}},
                {"$limit": 12},
                {"$unwind": "$cat"},
                {"$group": {
                    "_id": "$id",
                    "cat": {"$first": "$cat"}
                }},
                {"$facet": {
                    "nDocs": [{
                        "$count": "nDocs"
                    }],
                    "groupValues": [
                        {"$group": {
                            "_id": "$cat",
                            "total": {
                                "$sum": {"$toInt": 1}
                            }
                        }
                    }]
                }},
                {"$addFields": {
                    "nDocs": {
                        "$arrayElemAt": [
                            "$nDocs",
                            0
                        ]
                    }
                }},
                {"$unwind": "$groupValues"},
                {"$project": {
                    "_id": 0,
                    "category": "$groupValues._id",
                    "total": "$groupValues.total",
                    "percentage": {
                        "$round": [{
                        "$multiply": [
                            {"$divide": [
                                "$groupValues.total",
                                "$nDocs.nDocs"
                            ]}, 100
                        ]}, 2]
                    }
                }},
                {"$sort": {"percentage": -1}}
            ])
            posts_list = []
            for post in fetch_posts:
                posts_list.append(post)

            response = {'posts': posts_list}

            return {'result': response}
