from flask import Flask, jsonify, request, Blueprint
from flask_cors import CORS
from random import randint
from models import main_db, general_db
from bson.json_util import dumps
from flask_restful import Resource, reqparse, Api


app = Flask(__name__)
CORS(app, resources={r'/*': {'origins': '*'}}, supports_credentials=True)

artist_api_bp = Blueprint('artist_api', __name__)
artist_api = Api(artist_api_bp)

@artist_api_bp.route('/artist/info', methods=['GET'])
def get_artist_info():
    try:
        result = general_db.Artist.aggregate([
            # MID is string data type
            {"$match": {"MID": "1297"}},
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
        return jsonify(obj_list), 200
    except Exception as e:
        return dumps({'err': str(e)})

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