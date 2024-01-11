from models import main_db
from flask import jsonify, Blueprint
from bson.json_util import dumps
import datetime
from datetime import timedelta
from flask_restful import Resource, reqparse, Api


twitter_api_bp = Blueprint('twitter_api', __name__)
twitter_api = Api(twitter_api_bp)


class TwitterIndex(Resource):
    def get(self):
        posts_data = reqparse.RequestParser()
        posts_data.add_argument('end', type=lambda x: datetime.datetime.strptime(x, '%Y-%m-%d'), required=True,
                                location='args')
        posts_data.add_argument('range', type=str, required=True, location='args')
        data = posts_data.parse_args()
        end = data['end']
        range = data['range']

        # _temp_list = []

        if (range == 'month'):
            fetch_posts = main_db.twitter_index.aggregate([
                {"$sort": {"datetime": -1}},
                {"$match":
                     {"datetime":
                          {"$lte": end,
                           "$gt": end - datetime.timedelta(days=30)}
                      }},
                {"$project": {
                    "_id": 0,
                    "datetime": {
                        "$dateToString": {
                            "format": "%Y-%m-%d",
                            "date": "$datetime"
                        }
                    },
                    "name": "$name",
                    "username": "$username",
                    "follower": "$public_metrics.followers_count",
                    "following": "$public_metrics.following_count",
                    "tweets": "$public_metrics.tweet_count"
                }},
                {"$sort": {"datetime": 1}}
            ])
            posts_list = []
            for post in fetch_posts:
                posts_list.append(post)

            response = {'range': range,
                        'end': end.strftime("%Y-%m-%d"),
                        'posts': posts_list}

            return jsonify(response)
        elif (range == 'three_month'):
            fetch_posts = main_db.twitter_index.aggregate([
                {"$sort": {"datetime": -1}},
                {"$match":
                     {"datetime":
                          {"$lte": end,
                           "$gt": end - datetime.timedelta(days=90)}
                      }},
                {"$project": {
                    "_id": 0,
                    "datetime": {
                        "$dateToString": {
                            "format": "%Y-%m-%d",
                            "date": "$datetime"
                        }
                    },
                    "name": "$name",
                    "username": "$username",
                    "follower": "$public_metrics.followers_count",
                    "following": "$public_metrics.following_count",
                    "tweets": "$public_metrics.tweet_count"
                }},
                {"$sort": {"datetime": 1}}
            ])
            posts_list = []
            for post in fetch_posts:
                posts_list.append(post)

            response = {'range': range,
                        'end': end.strftime("%Y-%m-%d"),
                        'posts': posts_list}

            return jsonify(response)
        elif (range == 'six_month'):
            fetch_posts = main_db.twitter_index.aggregate([
                {"$sort": {"datetime": -1}},
                {"$match":
                     {"datetime":
                          {"$lte": end,
                           "$gt": end - datetime.timedelta(days=180)}
                      }},
                {"$project": {
                    "_id": 0,
                    "datetime": {
                        "$dateToString": {
                            "format": "%Y-%m-%d",
                            "date": "$datetime"
                        }
                    },
                    "name": "$name",
                    "username": "$username",
                    "follower": "$public_metrics.followers_count",
                    "following": "$public_metrics.following_count",
                    "tweets": "$public_metrics.tweet_count"
                }},
                {"$sort": {"datetime": 1}}
            ])
            posts_list = []
            for post in fetch_posts:
                posts_list.append(post)

            response = {'range': range,
                        'end': end.strftime("%Y-%m-%d"),
                        'posts': posts_list}

            return jsonify(response)
        elif (range == 'year'):
            fetch_posts = main_db.twitter_index.aggregate([
                {"$sort": {"datetime": -1}},
                {"$match":
                     {"datetime":
                          {"$lte": end,
                           "$gt": end - datetime.timedelta(days=365)}
                      }},
                {"$project": {
                    "_id": 0,
                    "datetime": {
                        "$dateToString": {
                            "format": "%Y-%m-%d",
                            "date": "$datetime"
                        }
                    },
                    "name": "$name",
                    "username": "$username",
                    "follower": "$public_metrics.followers_count",
                    "following": "$public_metrics.following_count",
                    "tweets": "$public_metrics.tweet_count"
                }},
                {"$sort": {"datetime": 1}}
            ])
            posts_list = []
            for post in fetch_posts:
                posts_list.append(post)

            response = {'range': range,
                        'end': end.strftime("%Y-%m-%d"),
                        'posts': posts_list}

            return jsonify(response)
        elif (range == 'overall'):
            fetch_posts = main_db.twitter_index.aggregate([
                {"$sort": {"datetime": -1}},
                {"$project": {
                    "_id": 0,
                    "datetime": {
                        "$dateToString": {
                            "format": "%Y-%m-%d",
                            "date": "$datetime"
                        }
                    },
                    "name": "$name",
                    "username": "$username",
                    "follower": "$public_metrics.followers_count",
                    "following": "$public_metrics.following_count",
                    "tweets": "$public_metrics.tweet_count"
                }},
                {"$sort": {"datetime": 1}}
            ])
            posts_list = []
            for post in fetch_posts:
                posts_list.append(post)

            response = {'range': range,
                        'end': end.strftime("%Y-%m-%d"),
                        'posts': posts_list}

            return jsonify(response)
        else:
            fetch_posts = main_db.twitter_index.aggregate([
                {"$sort": {"datetime": -1}},
                {"$match":
                     {"datetime":
                          {"$lte": end,
                           "$gt": end - datetime.timedelta(days=30)}
                      }},
                {"$project": {
                    "_id": 0,
                    "datetime": {
                        "$dateToString": {
                            "format": "%Y-%m-%d",
                            "date": "$datetime"
                        }
                    },
                    "name": "$name",
                    "username": "$username",
                    "follower": "$public_metrics.followers_count",
                    "following": "$public_metrics.following_count",
                    "tweets": "$public_metrics.tweet_count"
                }},
                {"$sort": {"datetime": 1}}
            ])
            posts_list = []
            for post in fetch_posts:
                posts_list.append(post)

            response = {'range': range,
                        'end': end.strftime("%Y-%m-%d"),
                        'posts': posts_list}

            return jsonify(response)
