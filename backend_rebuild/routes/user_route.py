'''
updated: 2025-08-04
user route
- create user (/v1/auth/register) -> POST
    - args:
        - firebase_id: string
        - name: string
        - image_url: string
        - email: string
        - tenant_id: string
        - followed_artist: list of artist ids
    - return: user object
    - error:
        - 400: bad request
        - 500: internal server error
- get user by firebase id (/v1/auth/firebase/<string:firebase_id>) -> GET
    - args:
        - firebase_id: string
    - return: user object
    - error:
        - 400: bad request
        - 500: internal server error
- update user (/v1/auth/user/<string:user_id>) -> PUT
    - args:
        - user_id: string
        - name: string
        - image_url: string
        - email: string
        - tenant_id: string
        - followed_artist: list of artist ids
    - return: user object
    - error:
        - 400: bad request
        - 500: internal server error
'''

from controllers.user_controller import UserController
from flask import Blueprint, jsonify, request
from flask_restful import Api

user_bp = Blueprint('user', __name__)
user_api = Api(user_bp)

@user_bp.route("/v1/auth/register", methods=["POST"])
def create_user():
    return UserController.create_user()

@user_bp.route("/v1/auth/firebase/<string:firebase_id>", methods=["GET"])
def get_user_by_firebase_id(firebase_id):
    try:
        result = UserController.get_user_by_firebase_id(firebase_id)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"err": str(e)}), 500

@user_bp.route("/v1/auth/user/<string:user_id>", methods=["PUT"])
def update_user(user_id):
    return UserController.update_user(user_id)

