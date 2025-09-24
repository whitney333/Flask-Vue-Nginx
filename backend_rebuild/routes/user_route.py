from controllers.user_controller import UserController
from flask import Blueprint, jsonify, request
from flask_restful import Api
from libs.utils import auth_required


user_bp = Blueprint('user', __name__)
user_api = Api(user_bp)

@user_bp.route("/v1/auth/me", methods=["GET"])
def get_user_profile(firebase_id):
    return UserController.get_user_info(firebase_id)

@user_bp.route("/v1/auth/signup", methods=["POST"])
def signup():
    return UserController.signup()

# used in RegisterDetailsView.vue to insert all user data
@user_bp.route("/v1/auth/register", methods=["POST"])
def create_user():
    return UserController.create_user()

@user_bp.route("/v1/auth/<string:firebase_id>", methods=["GET"])
def get_user_by_firebase_id(firebase_id):
    result = UserController.get_user_by_firebase_id(firebase_id)

    return result

@user_bp.route("/v1/followed_artists", methods=['GET'])
@auth_required
def get_user_followed_artist_by_id():
    result = UserController.get_user_followed_artist_by_id()
    return result

@user_bp.route("/v1/auth/check", methods=["POST"])
def check_user_exists():
    return UserController.check_user_exists()

@user_bp.route("/v1/company", methods=["GET"])
def get_all_tenant_company():
    result = UserController.get_all_tenant_company()

    return result

@user_bp.route("/v1/artists/<string:tenant_id>", methods=["GET"])
def get_all_artists_of_per_tenant(tenant_id):
    result = UserController.get_all_artist_by_tenant(tenant_id)

    return result
