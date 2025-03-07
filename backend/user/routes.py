from flask import jsonify, Blueprint, request
from flask_restful import Resource, reqparse, Api
import uuid

from pymongo import MongoClient
# from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
# import firebase_admin
# from firebase_admin import credentials, auth
from models import user_db

import os


user_api_bp = Blueprint("user_api", __name__)
user_api = Api(user_api_bp)

# configure mongodb
# client = MongoClient(os.environ["DB_HOST"],
#                      username=os.environ["DB_USERNAME"],
#                      password=os.environ["DB_PASSWORD"])
# db = client["user"]
# users_collection = db["users"]

# @user_api_bp.route("/auth/login", methods=["POST"])
# def login():
#     data = request.get_json()
#     email = data.get("email")
#     password = data.get("password")

#     user = users_collection.find_one({"email": email})

#     if user and bcrypt.checkpw(password.encode("utf-8"), user["password"]):
#         access_token = create_access_token(identity=email)
#         return jsonify(access_token=access_token), 200
#     else:
#         return jsonify({"msg": "Invalid email or password"}), 401

@user_api_bp.route("/v1/auth/register", methods=["POST", "OPTIONS"])
def register():
    
    data = request.get_json()

    firebase_id = data.get('firebaseId')
    name = data.get('name')
    company_name = data.get('companyName')
    artist_name = data.get('artistName')
    image_url = data.get('imageUrl')
    email = data.get('email')
    obj = {
        "firebaseId": firebase_id,
        "name": name,
        "companyName": company_name,
        "artistName": artist_name,
        "imageUrl": image_url,
        "email": email,
    }

    try:
        result = user_db.users.insert_one(obj)
        return jsonify({"status": "success"})

    except Exception as e:
        return jsonify(str(e))

@user_api_bp.route("/v1/auth/user/<firebaseId>", methods=["GET"])
def getUser(firebaseId):
    try:
        result = user_db.users.find_one({"firebaseId": firebaseId})

        if result:
            result["_id"] = str(result["_id"])

        return jsonify({"status": "success", "result": result})
    except Exception as e:
        return jsonify(str(e))



