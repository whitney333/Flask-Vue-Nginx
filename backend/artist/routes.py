from flask import Flask, jsonify, request, Blueprint
from flask_cors import CORS
from random import randint
from models import main_db, general_db, campaign_db
from bson.json_util import dumps
from flask_restful import Resource, reqparse, Api


app = Flask(__name__)
CORS(app, resources={r'/*': {'origins': '*'}}, supports_credentials=True)

artist_api_bp = Blueprint('artist_api', __name__)
artist_api = Api(artist_api_bp)

@artist_api_bp.route('/artist/members', methods=['GET'])
def get_members_info():
    try:
        result = general_db.Artist.aggregate([
            {"$unwind": "$BELONG_GROUP_MID"},
            {"$match": {"BELONG_GROUP_MID": "1297"}},
            #TODO Return more details of the artist
            {"$project": {
                "_id": 0,
                "mid": "$MID",
                "artist": "$ARTIST_NAME",
                "name_in_korean": "$NAME_IN_KOREAN",
                "debut_year": "$DEBUT_YEAR",
                "nation": "$NATION",
                "type": "$TYPE",
                "belong_to": "$BELONG_GROUP_MID",
            }}
        ])
        return dumps({'result': result})
    except Exception as e:
        return dumps({'err': str(e)})

@artist_api_bp.route('/artist/campaign', methods=['GET'])
def get_campaign():
    try:
        results = campaign_db.campaign_package.aggregate([
            {"$match": {"MID": "1297"}},
            {"$project": {
                "_id": 0,
                "cid": "$CID",
                "mid": "$MID",
                "region": "$REGION",
                "language": "$LANGUAGE",
                "start_date": {
                    "$dateToString": {
                        "format": "%Y-%m-%d",
                        "date": "$START_DATE"
                    }
                },
                "cost": "$COST",
                "currency": "$CURRENCY",
                "posts": "$POSTS"
            }},
            {"$group": {
                "_id": "$cid",
                "cid": {"$first": "$cid"},
                "mid": {"$first": "$mid"},
                "start_date": {"$first": "$start_date"},
                "region": {"$push": "$posts.REGION"},
                "language": {"$addToSet": "$posts.LANGUAGE"},
                "budget": {"$first": "$cost"},
                "currency": {"$first": "currency"},
                "total_reach": {
                    "$sum": {"$sum": "$posts.FOLLOWER"}
                },
                "posts": {"$first": "$posts"}
            }},
            {"$unwind": "$region"},
            {'$addFields': {'region': {'$setUnion': ['$region', []]}}},
            {"$unwind": "$language"},
            {'$addFields': {'language': {'$setUnion': ['$language', []]}}}
        ])
        posts_list = []
        for item in results:
            posts_list.append(item)
        return dumps({'result': posts_list})
    except Exception as e:
        return str(e)


class CampaignPackageDetail(Resource):
    def get(self):
        posts_data = reqparse.RequestParser()
        posts_data.add_argument('mid', type=str, required=True, location='args')
        posts_data.add_argument('cid', type=str, required=True, location='args')
        data = posts_data.parse_args()
        cid = data['cid']
        mid = data['mid']
        _temp_list = []

        try:
            fetch_posts = campaign_db.campaign_package.aggregate([
                {"$match": {"MID": mid}},
                {"$match": {"CID": cid}},
                {"$project": {
                    "_id": 0,
                    "cid": "$CID",
                    "mid": "$MID",
                    "region": "$REGION",
                    "language": "$LANGUAGE",
                    "start_date": {
                        "$dateToString": {
                            "format": "%Y-%m-%d",
                            "date": "$START_DATE"
                        }
                    },
                    "cost": "$COST",
                    "currency": "$CURRENCY",
                    "posts": "$POSTS"
                }},
                {"$group": {
                    "_id": "$cid",
                    "cid": {"$first": "$cid"},
                    "mid": {"$first": "$mid"},
                    "start_date": {"$first": "$start_date"},
                    "region": {"$push": "$posts.REGION"},
                    "language": {"$addToSet": "$posts.LANGUAGE"},
                    "budget": {"$first": "$cost"},
                    "currency": {"$first": "$currency"},
                    "total_reach": {
                        "$sum": {"$sum": "$posts.FOLLOWER"}
                    },
                    "posts": {"$first": "$posts"}
                }},
                {"$unwind": "$region"},
                {'$addFields': {'region': {'$setUnion': ['$region', []]}}},
                {"$unwind": "$language"},
                {'$addFields': {'language': {'$setUnion': ['$language', []]}}}
            ])
            posts_list = []
            for post in fetch_posts:
                posts_list.append(post)
            response = {'mid': mid,
                        'cid': cid,
                        'results': posts_list[0]}

            return jsonify(response)
        except Exception as e:
            return dumps({'err': str(e)})


class ArtistInfo(Resource):
    def get(self):
        posts_data = reqparse.RequestParser()
        posts_data.add_argument('mid', type=str, required=True, location='args')
        data = posts_data.parse_args()
        mid = data['mid']
        _temp_list = []

        try:
            result = general_db.Artist.aggregate([
                # MID is string data type
                {"$match": {"MID": mid}},
                {"$unwind": "$COMPANIES"},
                {"$project": {
                    "_id": 0,
                    "mid": "$MID",
                    "artist": "$ARTIST_NAME",
                    "name_in_korean": "$NAME_IN_KOREAN",
                    "debut_year": "$DEBUT_YEAR",
                    "debut_date": {
                        "$dateToString": {
                            "format": "%Y-%m-%d",
                            "date": "$DEBUT_DATE"
                        }},
                    "birth": {
                        "$dateToString": {
                            "format": "%Y-%m-%d",
                            "date": "$BIRTH"
                        }},
                    "nation": "$NATION",
                    "type": "$TYPE",
                    "belong_to": "$BELONG_GROUP_MID",
                    "labels": "$COMPANIES.COMPANY",
                    "fandom": "$FANDOM",
                    "color": "$COLOR",
                    "social_medias": "$SOCIAL_MEDIAS",
                    "music_plt": "$MUSIC_PLATFORMS",
                    "image": "$IMAGE"
                }}
            ])
            obj_list = []
            for item in result:
                obj_list.append(item)
            response = {'mid': mid,
                        'results': obj_list[0]}
            return jsonify(response)
        except Exception as e:
            return dumps({'err': str(e)})
