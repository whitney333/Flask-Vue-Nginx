from flask import jsonify, Blueprint, request
from flask_restful import Resource, reqparse, Api
import bcrypt
from pymongo import MongoClient
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import firebase_admin
from firebase_admin import credentials, auth
import os


user_api_bp = Blueprint("user_api", __name__)
user_api = Api(user_api_bp)

# configure mongodb
client = MongoClient(os.environ["DB_HOST"],
                     username=os.environ["DB_USERNAME"],
                     password=os.environ["DB_PASSWORD"])
db = client["user"]
users_collection = db["users"]

@user_api_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    user = users_collection.find_one({"email": email})

    if user and bcrypt.checkpw(password.encode("utf-8"), user["password"]):
        access_token = create_access_token(identity=email)
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({"msg": "Invalid email or password"}), 401
