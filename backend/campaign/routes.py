from libs.utils import getIdFromFirebaseID
from firebase.firebase_auth import verify_firebase_token
from models import campaign_db
from flask import jsonify, Blueprint, request
from bson.json_util import dumps
import datetime
from datetime import timedelta
from flask_restful import Resource, reqparse, Api
from libs.utils import require_auth

campaign_api_bp = Blueprint('campaign_api', __name__)
campaign_api = Api(campaign_api_bp)

@campaign_api_bp.route('/v1/campaign/posts', methods=['GET'])
@require_auth
def get_campaign_posts():
    try:
        userId = request.user_id
        # get all posts
        posts = campaign_db.posts.find({'userId': userId})
        return dumps(posts), 200
    except Exception as e:
        return dumps({'err': str(e)})


@campaign_api_bp.route('/v1/campaign/post/{id}', methods=['POST'])
@require_auth
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
@require_auth
def post_campign_post():
    try:
        data = request.json()
        data['userId'] = request.user_id
        data['created_at'] = datetime.datetime.now()
        post = campaign_db.posts.insert_one(data)
        return dumps(post), 200
    except Exception as e:
        return dumps({'err': str(e)})


@campaign_api_bp.route('/v1/campaign/post/{id}', methods=['PUT'])
@require_auth
def put_campign_post(id: str):
    try:
        # get post by id
        post = campaign_db.posts.update_one({'_id': id}, {'$set': request.json})
        return dumps(post), 200
    except Exception as e:
        return dumps({'err': str(e)})