from controllers.user_controller import UserController
from flask import Blueprint, jsonify, request
from flask_restful import Api
from libs.utils import auth_required


user_bp = Blueprint('user', __name__)
user_api = Api(user_bp)

@user_bp.route("/v1/auth/me", methods=["GET"])
@auth_required
def get_user_profile():
    return UserController.get_user_info()

@user_bp.route("/v1/auth/signup", methods=["POST"])
def signup():
    return UserController.signup()

# used in RegisterDetailsView.vue to insert all user data
@user_bp.route("/v1/auth/register", methods=["POST"])
@auth_required
def create_user():
    return UserController.create_user()

@user_bp.route("/v1/auth/<string:firebase_id>", methods=["GET"])
@auth_required
def get_user_by_firebase_id(firebase_id):
    result = UserController.get_user_by_firebase_id(firebase_id)

    return result

@user_bp.route("/v1/auth/check", methods=["POST"])
@auth_required
def check_user_exists():
    return UserController.check_user_exists()

@user_bp.route("/v1/auth/check_admin", methods=["POST"])
@auth_required
def check_is_admin():
    return UserController.check_is_admin()

@user_bp.route("/v1/company", methods=["GET"])
@auth_required
def get_all_tenant_company():
    result = UserController.get_all_tenant_company()

    return result

@user_bp.route("/v1/artists/<string:tenant_id>", methods=["GET"])
@auth_required
def get_all_artists_of_per_tenant(tenant_id):
    result = UserController.get_all_artist_by_tenant(tenant_id)

    return result

@user_bp.route("/me", methods=["GET"])
@auth_required
def get_me():
    return UserController.get_me()

@user_bp.route("/v1/followed_artists", methods=["PUT"])
@auth_required
def update_followed_artists():
    return UserController.update_followed_artists()

@user_bp.route("/v1/followed_artists", methods=['GET'])
@auth_required
def get_user_followed_artists():
    result = UserController.get_user_followed_artist()

    return result
