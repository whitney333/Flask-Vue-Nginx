from models import main_db
from flask import jsonify, Blueprint
from bson.json_util import dumps
from flask_restful import Resource, reqparse, Api
import datetime
from datetime import timedelta


bilibili_api_bp = Blueprint('bilibili_api', __name__)
bilibili_api = Api(bilibili_api_bp)

# add charts: total likes/ comments/ collects/ shares/ views/ danmus/ coins
@bilibili_api_bp.route('/bilibili/chart', methods=['GET'])
def get_bilibili_index():
    try:
        result = main_db.bilibili_video_info.aggregate([
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
                "view": "$data.view",
                "danmu": "$data.danmu",
                "comment": "$data.comment",
                "collect": "$data.collect",
                "coin": "$data.coin",
                "share": "$data.share",
                "like": "$data.like"
            }},
            {"$group": {
                "_id": "$datetime",
                "video_num": {"$sum": {"$toInt": 1}},
                "total_like": {"$sum": "$like"},
                "total_comment": {"$sum": "$comment"},
                "total_share": {"$sum": "$share"},
                "total_views": {"$sum": "$view"},
                "total_danmu": {"$sum": "$danmu"},
                "total_collect": {"$sum": "$collect"},
                "total_coin": {"$sum": "$coin"}
            }},
            {"$sort": {"_id": 1}},
            {"$addFields": {
                "sub_total": {
                    "$sum": ["$total_like", "$total_comment", "$total_share", "$total_danmu", "$total_collect",
                             "$total_coin"]}
            }},
            {"$project": {
                "datetime": "$_id",
                "video_num": "$video_num",
                "eng_rate": {
                    "$round": [
                        {"$multiply": [{"$divide": ["$sub_total", "$total_views"]}, 100]}, 2
                    ]
                },
                "total_like": "$total_like",
                "total_comment": "$total_comment",
                "total_share": "$total_share",
                "total_views": "$total_views",
                "total_danmu": "$total_danmu",
                "total_collect": "$total_collect",
                "total_coin": "$total_coin",
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
                    "$round": [{"$divide": ["$total_views", "$video_num"]}, 2]
                },
                "avg_danmu": {
                    "$round": [{"$divide": ["$total_danmu", "$video_num"]}, 2]
                },
                "avg_collect": {
                    "$round": [{"$divide": ["$total_collect", "$video_num"]}, 2]
                },
                "avg_coin": {
                    "$round": [{"$divide": ["$total_coin", "$video_num"]}, 2]
                }
            }}
        ])
        return dumps({'result': result})
    except Exception as e:
        return dumps({'error': str(e)})

@bilibili_api_bp.route('/bilibili/posts', methods=['GET'])
def get_bilibili_posts():
    '''
    Get bilibili all videos
    :return: videos
    '''
    try:
        results = main_db.bilibili_video_info.aggregate([
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
                "data": "$data"
            }}
        ])
        return dumps({'result': results})
    except Exception as e:
        return dumps({'error': str(e)})


class BilibiliPost(Resource):
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
        posts_count_cur = main_db.bilibili_video_info.aggregate([
            {"$sort": {"datetime": -1}},
            {"$limit": 1},
            {"$unwind": "$data"},
            {"$group": {
                "_id": "total",
                "count": {"$sum": {"$toInt": 1}}
            }}
        ])

        for item in posts_count_cur:
            _temp_list.append(item['count'])

        posts_count = _temp_list[0]

        # Sort By: Date/ Most Likes/ Most Comments/ Most Shares/ Most Coins/ Most Collects/ Most Danmus/ Most Views
        # case 1: Date
        if (sort == 'date'):
            # fetch all posts
            fetch_posts = main_db.bilibili_video_info.aggregate([
                {"$sort": {"datetime": -1}},
                {"$limit": 1},
                {"$unwind": "$data"},
                {"$project": {
                    "_id": 0,
                    "title": "$data.title",
                    "bvid": "$data.bvid",
                    "upload_date": {
                        "$dateToString": {
                            "format": "%Y-%m-%d",
                            "date": "$data.upload_date"
                        }},
                    "view": "$data.view",
                    "danmu": "$data.danmu",
                    "comment": "$data.comment",
                    "collect": "$data.collect",
                    "coin": "$data.coin",
                    "share": "$data.share",
                    "like": "$data.like",
                    "image": "$data.new_image_url",
                    "url": "$data.url"
                }},
                {"$sort": {"upload_date": -1}},
                {"$skip": int(page_limit) * (int(page) - 1)},
                {"$limit": int(page_limit)}
            ])

            posts_list = []
            for post in fetch_posts:
                posts_list.append(post)

            response = {'total_posts_count': posts_count, 'page': int(page), 'perPage': int(page_limit), 'sort': sort, 'posts': posts_list}

            return jsonify(response)
        elif (sort == 'like'):
            fetch_posts = main_db.bilibili_video_info.aggregate([
                {"$sort": {"datetime": -1}},
                {"$limit": 1},
                {"$unwind": "$data"},
                {"$project": {
                    "_id": 0,
                    "title": "$data.title",
                    "bvid": "$data.bvid",
                    "upload_date": {
                        "$dateToString": {
                            "format": "%Y-%m-%d",
                            "date": "$data.upload_date"
                        }},
                    "view": "$data.view",
                    "danmu": "$data.danmu",
                    "comment": "$data.comment",
                    "collect": "$data.collect",
                    "coin": "$data.coin",
                    "share": "$data.share",
                    "like": "$data.like",
                    "image": "$data.new_image_url",
                    "url": "$data.url"
                }},
                {"$sort": {"like": -1}},
                {"$skip": int(page_limit) * (int(page) - 1)},
                {"$limit": int(page_limit)}
            ])

            posts_list = []
            for post in fetch_posts:
                posts_list.append(post)

            response = {'total_posts_count': posts_count, 'page': int(page), 'perPage': int(page_limit), 'sort': sort, 'posts': posts_list}

            return jsonify(response)
        elif (sort == 'comment'):
            fetch_posts = main_db.bilibili_video_info.aggregate([
                {"$sort": {"datetime": -1}},
                {"$limit": 1},
                {"$unwind": "$data"},
                {"$project": {
                    "_id": 0,
                    "title": "$data.title",
                    "bvid": "$data.bvid",
                    "upload_date": {
                        "$dateToString": {
                            "format": "%Y-%m-%d",
                            "date": "$data.upload_date"
                        }},
                    "view": "$data.view",
                    "danmu": "$data.danmu",
                    "comment": "$data.comment",
                    "collect": "$data.collect",
                    "coin": "$data.coin",
                    "share": "$data.share",
                    "like": "$data.like",
                    "image": "$data.new_image_url",
                    "url": "$data.url"
                }},
                {"$sort": {"comment": -1}},
                {"$skip": int(page_limit) * (int(page) - 1)},
                {"$limit": int(page_limit)}
            ])

            posts_list = []
            for post in fetch_posts:
                posts_list.append(post)

            response = {'total_posts_count': posts_count, 'page': int(page), 'perPage': int(page_limit), 'sort': sort, 'posts': posts_list}

            return jsonify(response)
        elif (sort == 'share'):
            fetch_posts = main_db.bilibili_video_info.aggregate([
                {"$sort": {"datetime": -1}},
                {"$limit": 1},
                {"$unwind": "$data"},
                {"$project": {
                    "_id": 0,
                    "title": "$data.title",
                    "bvid": "$data.bvid",
                    "upload_date": {
                        "$dateToString": {
                            "format": "%Y-%m-%d",
                            "date": "$data.upload_date"
                        }},
                    "view": "$data.view",
                    "danmu": "$data.danmu",
                    "comment": "$data.comment",
                    "collect": "$data.collect",
                    "coin": "$data.coin",
                    "share": "$data.share",
                    "like": "$data.like",
                    "image": "$data.new_image_url",
                    "url": "$data.url"
                }},
                {"$sort": {"share": -1}},
                {"$skip": int(page_limit) * (int(page) - 1)},
                {"$limit": int(page_limit)}
            ])

            posts_list = []
            for post in fetch_posts:
                posts_list.append(post)

            response = {'total_posts_count': posts_count, 'page': int(page), 'perPage': int(page_limit), 'sort': sort, 'posts': posts_list}

            return jsonify(response)
        elif (sort == 'coin'):
            fetch_posts = main_db.bilibili_video_info.aggregate([
                {"$sort": {"datetime": -1}},
                {"$limit": 1},
                {"$unwind": "$data"},
                {"$project": {
                    "_id": 0,
                    "title": "$data.title",
                    "bvid": "$data.bvid",
                    "upload_date": {
                        "$dateToString": {
                            "format": "%Y-%m-%d",
                            "date": "$data.upload_date"
                        }},
                    "view": "$data.view",
                    "danmu": "$data.danmu",
                    "comment": "$data.comment",
                    "collect": "$data.collect",
                    "coin": "$data.coin",
                    "share": "$data.share",
                    "like": "$data.like",
                    "image": "$data.new_image_url",
                    "url": "$data.url"
                }},
                {"$sort": {"coin": -1}},
                {"$skip": int(page_limit) * (int(page) - 1)},
                {"$limit": int(page_limit)}
            ])

            posts_list = []
            for post in fetch_posts:
                posts_list.append(post)

            response = {'total_posts_count': posts_count, 'page': int(page), 'perPage': int(page_limit), 'sort': sort, 'posts': posts_list}

            return jsonify(response)
        elif (sort == 'collect'):
            fetch_posts = main_db.bilibili_video_info.aggregate([
                {"$sort": {"datetime": -1}},
                {"$limit": 1},
                {"$unwind": "$data"},
                {"$project": {
                    "_id": 0,
                    "title": "$data.title",
                    "bvid": "$data.bvid",
                    "upload_date": {
                        "$dateToString": {
                            "format": "%Y-%m-%d",
                            "date": "$data.upload_date"
                        }},
                    "view": "$data.view",
                    "danmu": "$data.danmu",
                    "comment": "$data.comment",
                    "collect": "$data.collect",
                    "coin": "$data.coin",
                    "share": "$data.share",
                    "like": "$data.like",
                    "image": "$data.new_image_url",
                    "url": "$data.url"
                }},
                {"$sort": {"collect": -1}},
                {"$skip": int(page_limit) * (int(page) - 1)},
                {"$limit": int(page_limit)}
            ])

            posts_list = []
            for post in fetch_posts:
                posts_list.append(post)

            response = {'total_posts_count': posts_count, 'page': int(page), 'perPage': int(page_limit), 'sort': sort, 'posts': posts_list}

            return jsonify(response)
        elif (sort == 'view'):
            fetch_posts = main_db.bilibili_video_info.aggregate([
                {"$sort": {"datetime": -1}},
                {"$limit": 1},
                {"$unwind": "$data"},
                {"$project": {
                    "_id": 0,
                    "title": "$data.title",
                    "bvid": "$data.bvid",
                    "upload_date": {
                        "$dateToString": {
                            "format": "%Y-%m-%d",
                            "date": "$data.upload_date"
                        }},
                    "view": "$data.view",
                    "danmu": "$data.danmu",
                    "comment": "$data.comment",
                    "collect": "$data.collect",
                    "coin": "$data.coin",
                    "share": "$data.share",
                    "like": "$data.like",
                    "image": "$data.new_image_url",
                    "url": "$data.url"
                }},
                {"$sort": {"view": -1}},
                {"$skip": int(page_limit) * (int(page) - 1)},
                {"$limit": int(page_limit)}
            ])

            posts_list = []
            for post in fetch_posts:
                posts_list.append(post)

            response = {'total_posts_count': posts_count, 'page': int(page), 'perPage': int(page_limit), 'sort': sort, 'posts': posts_list}

            return jsonify(response)
        elif (sort == 'danmu'):
            fetch_posts = main_db.bilibili_video_info.aggregate([
                {"$sort": {"datetime": -1}},
                {"$limit": 1},
                {"$unwind": "$data"},
                {"$project": {
                    "_id": 0,
                    "title": "$data.title",
                    "bvid": "$data.bvid",
                    "upload_date": {
                        "$dateToString": {
                            "format": "%Y-%m-%d",
                            "date": "$data.upload_date"
                        }},
                    "view": "$data.view",
                    "danmu": "$data.danmu",
                    "comment": "$data.comment",
                    "collect": "$data.collect",
                    "coin": "$data.coin",
                    "share": "$data.share",
                    "like": "$data.like",
                    "image": "$data.new_image_url",
                    "url": "$data.url"
                }},
                {"$sort": {"danmu": -1}},
                {"$skip": int(page_limit) * (int(page) - 1)},
                {"$limit": int(page_limit)}
            ])

            posts_list = []
            for post in fetch_posts:
                posts_list.append(post)

            response = {'total_posts_count': posts_count, 'page': int(page), 'perPage': int(page_limit), 'sort': sort, 'posts': posts_list}

            return jsonify(response)
        else:
            # fetch all posts
            fetch_posts = main_db.bilibili_video_info.aggregate([
                {"$sort": {"datetime": -1}},
                {"$limit": 1},
                {"$unwind": "$data"},
                {"$project": {
                    "_id": 0,
                    "title": "$data.title",
                    "bvid": "$data.bvid",
                    "upload_date": {
                        "$dateToString": {
                            "format": "%Y-%m-%d",
                            "date": "$data.upload_date"
                        }},
                    "view": "$data.view",
                    "danmu": "$data.danmu",
                    "comment": "$data.comment",
                    "collect": "$data.collect",
                    "coin": "$data.coin",
                    "share": "$data.share",
                    "like": "$data.like",
                    "image": "$data.new_image_url",
                    "url": "$data.url"
                }},
                {"$sort": {"upload_date": -1}},
                {"$skip": int(page_limit) * (int(page) - 1)},
                {"$limit": int(page_limit)}
            ])

            posts_list = []
            for post in fetch_posts:
                posts_list.append(post)

            response = {'total_posts_count': posts_count, 'page': int(page), 'perPage': int(page_limit), 'sort': sort, 'posts': posts_list}

            return jsonify(response)
