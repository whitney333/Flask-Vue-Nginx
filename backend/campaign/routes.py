from libs.utils import getIdFromFirebaseID
from firebase.firebase_auth import verify_firebase_token
from models import campaign_db
from flask import jsonify, Blueprint, request
from bson.json_util import dumps
import datetime
from datetime import timedelta
from flask_restful import Resource, reqparse, Api

campaign_api_bp = Blueprint('campaign_api', __name__)
campaign_api = Api(campaign_api_bp)


@campaign_api_bp.route('/v1/campaign/posts', methods=['GET'])
def get_campaign_posts():
    try:
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return jsonify({"error": "Unauthorized"}), 401

        token = auth_header.split(" ")[1]
        decoded_token = verify_firebase_token(token)

        if not decoded_token:
            return jsonify({"error": "Invalid token"}), 401

        firebaseId = decoded_token['uid']
        userId = getIdFromFirebaseID(firebaseId)
        # get all posts
        posts = campaign_db.posts.find({'userId': userId})
        return dumps(posts), 200
    except Exception as e:
        return dumps({'err': str(e)})


@campaign_api_bp.route('/v1/campaign/post/{id}', methods=['POST'])
def get_campign_post(id: str):
    """_summary_

    Args:
        id (str): _description_

    Returns:
        _type_: _description_
    """
    try:
        # get post by id
        post = campaign_db.posts.find_one({'_id': id})
        return dumps(post), 200
    except Exception as e:
        return dumps({'err': str(e)})


@campaign_api_bp.route('/v1/campaign/post', methods=['POST'])
def post_campign_post():
    try:
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return jsonify({"error": "Unauthorized"}), 401

        token = auth_header.split(" ")[1]
        decoded_token = verify_firebase_token(token)

        if not decoded_token:
            return jsonify({"error": "Invalid token"}), 401

        data = request.get_json()
        firebaseId = decoded_token['uid']
        data['userId'] = getIdFromFirebaseID(firebaseId)
        data['created_at'] = datetime.datetime.now()
        post = campaign_db.posts.insert_one(data)
        return dumps(post), 200
    except Exception as e:
        return dumps({'err': str(e)})


@campaign_api_bp.route('/v1/campaign/post/{id}', methods=['PUT'])
def put_campign_post(id: str):
    try:
        # get post by id
        post = campaign_db.posts.update_one({'_id': id}, {'$set': request.json})
        return dumps(post), 200
    except Exception as e:
        return dumps({'err': str(e)})