from models.user_model import Users
from models.tenant_model import Tenant
from models.artist_model import Artists
import datetime
from mongoengine import ValidationError, DoesNotExist
from flask import request, jsonify, g
from functools import wraps
from firebase_admin import auth
from bson import json_util
import json


class UserController:

    def get_user_info(firebase_id):
       try:
           user = Users.objects(firebase_id="uSI8I0epjHVmFpEWMNyb9g43pv22").first()
           print(user)
           if user:
               return jsonify({
                   "status": "success",
                   "data": "2"
               }), 200
           else:
               return jsonify({
                   "status": "error",
                   "message": "User not found"
               }), 404
       except Exception as e:
           return jsonify({
               "err": str(e)
           }), 500

    def get_user_by_firebase_id(firebase_id):
        """
        Get a user by Firebase ID
        :return:
        """
        try:
            # return QuerySet
            user = Users.objects(firebase_id=firebase_id).exclude("id").first()

            if not user:
                return jsonify({
                    "error": "No user data found"
                }), 404

            return jsonify({
                "status": "success",
                "data": json.loads(user.to_json())
            }), 200
        except Exception as e:
            return jsonify({
                "error": str(e)
            }), 500

    @classmethod
    def signup(cls):
        try:
            # get firebase token from header
            id_token = request.headers.get("Authorization", "").replace("Bearer ", "")
            # print(id_token)
            if not id_token:
                return jsonify({"error": "Missing token"}), 401

            # auth Firebase token
            decoded_token = auth.verify_id_token(id_token)
            uid = decoded_token["uid"]

            # get email
            data = request.get_json()
            # print(data)
            email = data.get("email")

            if not email:
                return jsonify({"error": "Missing email"}), 400

            # check if email exists or not
            if Users.objects(email=email).first():
                return jsonify({"message": "User already exists"}), 200

            # store in database
            user = Users(
                firebase_id=uid,
                email=email
            )
            user.save()

            return jsonify({
                "message": "User registered successfully",
                "user": {
                    "uid": user.uid,
                    "email": user.email,
                    "role": user.role,
                    "created_at": user.created_at
                }
            }), 201

        except Exception as e:
            return jsonify({
                "err": str(e)
            }), 500

    @classmethod
    def create_user(cls):
        # get data
        data = request.get_json()
        print(data)
        try:
            if not data.get("firebaseId") or not data.get("name") or not data.get("email") or not data.get("tenant") or not data.get("followed_artist"):
                return jsonify({
                    "error": "Missing required fields"
                }), 400
            # user already exists
            if Users.objects(firebase_id=data.get("firebaseId")).first():
                return jsonify({
                    "error": "User already exists"
                }), 400

            # get tenant id
            tenant_id = data.get("tenant")
            tenant = Tenant.objects(id=tenant_id).first()
            if not tenant:
                return jsonify({
                    "error": "Tenant not found"
                }), 404

            artist_ids = data.get("followed_artist")
            if not artist_ids:
                return jsonify({
                    "error": "Followed artist is required"
                }), 400

            # artists = Artists.objects(artist_id__in=artist_ids)
            # if not artists or len(artists) != len(artist_ids):
            #     return jsonify({
            #         "error": "Artist not found"
            #     }), 404
            # if login via email/ pwd
            # image default: None
            image_url = data.get("image_url")
            if not image_url:
                image_url = "https://mishkan-ltd.s3.ap-northeast-2.amazonaws.com/web-dist/user-circle-96.png"

            new_user = Users(
                firebase_id = data.get("firebaseId"),
                name = data.get("name"),
                image_url = image_url,
                email = data.get("email"),
                tenant = data.get("tenant"),
                followed_artist = data.get("followed_artist"),
                created_at = data.get("created_at"),
                last_login_at = data.get("last_login_at"),
                admin = False
            )
            new_user.save()

            return jsonify({
                "status": "success",
                "message": "User created successfully",
            }), 201
        except Exception as e:
            return jsonify({
                "error": str(e)
            }), 500

    def update_user(user_id):
        data  = request.get_json()
        try:
            user = Users.objects(id=user_id).first()
            if user:
                user.update(**data)
                user.save()
                return jsonify({
                    "status": "success",
                    "message": "User updated successfully"
                }), 200
            else:
                return jsonify({
                    "error": "User not found"
                }), 404
        except Exception as e:
            return jsonify({
                "error": str(e)
            }), 500

    @staticmethod
    def login_user():
        data = request.json.get("IdToken")


        try:
            decoded = auth.verify_id_token(data)
            firebase_id = decoded["firebase_id"]
            name = decoded["name"]
            company_name = decoded["company_name"]
            artist_name = decoded["artist_name"]
            image_url = decoded["image_url"]
            email = decoded["email"]

            user = Users.objects(firebase_id=firebase_id).first()
            if not user:
                user = Users(
                    # user_id = user_id,
                    firebase_id=firebase_id,
                    name=name,
                    company_name=company_name,
                    artist_name=artist_name,
                    image_url=image_url,
                    email=email,
                    admin=False
                )
                user.save()

            return jsonify({
                "status": "success",
                "message": "User created successfully",
            }), 201

        except Exception as e:
            return jsonify({
                "success": False,
                "error": str(e)
            }), 401

    @classmethod
    def get_user_followed_artist_by_id(cls):
        if not getattr(g, "firebase_id", None):
            return jsonify({"status": "error", "message": "Unauthorized"}), 401

        user = Users.objects(firebase_id=g.firebase_id).first()
        print("g.firebase_id: ", g.firebase_id)
        if not user:
            return jsonify({
                "status": "error",
                "message": "User not found"
            }), 404
        followed = getattr(user, "followed_artist", []) or []
        # find all followed artist. return Artist object
        # followed = user.followed_artist

        artist_data = list()
        # get user followed artist
        for artist in followed:
            artist_data.append({
                "id": str(artist.id) if artist.id else None,
                "artist_id": artist.artist_id,
                "english_name": artist.english_name,
                "korean_name": artist.korean_name,
                "image": artist.image_url
            })

        return jsonify({
            "status": "success",
            "data": artist_data
        }), 200

    @classmethod
    def check_user_exists(cls):
        data = request.get_json()

        firebase_uid = data.get("firebase_id")

        # firebase_uid = g.firebase_id
        user = Users.objects(firebase_id=firebase_uid).first()

        if user:

            # print(user)
            return jsonify({
                "exists": True,
                "admin": user.admin
            }), 200
        else:
            # no user data in database yet
            return jsonify({
                "exists": False
            }), 200

    @staticmethod
    def get_all_tenant_company():
        """
        Get all companies name
        :return:
        """
        tenants = Tenant.objects().order_by("tenant_name")
        company = [
            {"tenant_name": t.tenant_name,
             "tenant_id": str(t.id) } for t in tenants]

        return jsonify({
            "status": "success",
            "data": company
        }), 200

    def get_all_artist_by_tenant(tenant_id):
        artists = Artists.objects(tenant_id=tenant_id).order_by("english_name")
        artist_names = [
            {"artist_name": a.english_name,
             "korean_name": a.korean_name,
             "artist_id": a.artist_id,
             "artist_objId": str(a.id),
             "imageURL": a.image_url} for a in artists
        ]

        return jsonify({
            "status": "success",
            "data": artist_names
        }), 200
