from controllers.user_controller import UserController
from flask import Blueprint, jsonify, request
from flask_restful import Api

user_bp = Blueprint('user', __name__)
user_api = Api(user_bp)

@user_bp.route("/v1/auth/register", methods=["POST"])
def create_user():
    return UserController.create_user()

@user_bp.route("/firebase/<string:firebase_id>", methods=["GET"])
def get_user_by_firebase_id(firebase_id):
    try:
        result = UserController.get_by_firebase_id(firebase_id)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"err": str(e)}), 500
