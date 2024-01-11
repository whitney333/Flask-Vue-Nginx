from models import news_db
from flask import jsonify, Blueprint
from bson.json_util import dumps
from flask_restful import Resource, reqparse, Api
import datetime
from datetime import timedelta
from pytrends.request import TrendReq


news_api_bp = Blueprint('news_api', __name__)
news_api = Api(news_api_bp)

@news_api_bp.route('/google-trends/youtube-rising-query', methods=['GET'])
def getRisingQuery():
    try:
        pytrend = TrendReq()
        # Daily: 'now #-d' where # is the number of days from that date to pull data for
        # %2Fg%2F11rkc8vfp7
        pytrend.build_payload(kw_list=['/g/11ft_dg48v'], timeframe='now 7-d', gprop='youtube')
        # sug = pytrend.suggestions('Mirani')
        # print(sug)

        # call related_queries method
        relate_query = pytrend.related_queries()
        # find related rising query
        df = relate_query['/g/11ft_dg48v']['rising']

        # transpose dataframe to dict
        df = df.T.to_dict('records')

        # fetch first column in df: query
        query = df[0]
        # fetch second column in df: search value
        q_value = df[1]

        # create two blank lists to format query & value
        query_list = []
        value_list = []
        for value in query.values():
            query_list.append(value)
        for value in q_value.values():
            value_list.append(value)
        #list_of_dict = [{'key1': L1, 'key2': L2} for (L1,L2) in zip(list_1,list_2)]
        result = [{'query': L1, 'value': L2} for (L1,L2) in zip(query_list, value_list)]

        return jsonify(result[:10]), 200
    except Exception as e:
        return dumps({'err': str(e)})

@news_api_bp.route('/google-trends/web-rising-query', methods=['GET'])
def getWebRisingQuery():
    try:
        pytrend = TrendReq()
        # Daily: 'now #-d' where # is the number of days from that date to pull data for
        pytrend.build_payload(kw_list=['/g/11ft_dg48v'], timeframe='now 7-d')
        # sug = pytrend.suggestions('Mirani')
        # print(sug)

        # call related_queries method
        relate_query = pytrend.related_queries()
        # find related rising query
        df = relate_query['/g/11ft_dg48v']['rising']

        # transpose dataframe to dict
        df = df.T.to_dict('records')

        # fetch first column in df: query
        query = df[0]
        # fetch second column in df: search value
        q_value = df[1]

        # create two blank lists to format query & value
        query_list = []
        value_list = []
        for value in query.values():
            query_list.append(value)
        for value in q_value.values():
            value_list.append(value)
        # list_of_dict = [{'key1': L1, 'key2': L2} for (L1,L2) in zip(list_1,list_2)]
        result = [{'query': L1, 'value': L2} for (L1, L2) in zip(query_list, value_list)]

        return jsonify(result[:10]), 200
    except Exception as e:
        return dumps({'err': str(e)})

class TheQooHot(Resource):
    def get(self):
        posts_data = reqparse.RequestParser()
        posts_data.add_argument('page', type=str, required=True, help='Page number is required', location='args')
        posts_data.add_argument('limit', type=str, required=True, help='Limit is required', location='args')
        posts_data.add_argument('q', type=str, required=True, location='args')
        data = posts_data.parse_args()

        page = data['page']
        page_limit = data['limit']
        q = data['q']

        # Sort By: Date range
        # fetch all posts
        fetch_posts = news_db.theqoo.aggregate([
            {"$sort": {"created_date": -1}},
            {"$match": {
                "title": {"$regex": q}
            }},
            {"$project": {
                "_id": 0,
                "url": "$url",
                "title": "$title",
                "views": "$views",
                "comments": "$comments",
                "date": {
                    "$dateToString": {
                        "format": "%Y-%m-%d",
                        "date": "$created_date"
                    }
                },
            }},
            # {"$match":
            #      {"datetime":
            #           {"$lte": datetime.datetime.now(),
            #            "$gt": datetime.datetime.now() - datetime.timedelta(days=8)}
            #       }},
            # {"$project": {
            #     "_id": 0,
            #     "url": "$url",
            #     "title": "$title",
            #     "views": "$views",
            #     "comments": "$comments",
            #     "date": {
            #         "$dateToString": {
            #             "format": "%Y-%m-%d",
            #             "date": "$created_date"
            #         }
            #     },
            # }}
            {"$skip": int(page_limit) * (int(page) - 1)},
            {"$limit": int(page_limit)}
        ])

        posts_list = []
        for post in fetch_posts:
            posts_list.append(post)

        response = {'q': q, 'page': int(page), 'perPage': int(page_limit), 'posts': posts_list}

        return jsonify(response)
