from models.user_model import Users
from models.tenant_model import Tenant
from models.artist_model import Artists
from services.user_service import UserService
import datetime
from mongoengine import ValidationError, DoesNotExist
from flask import request, jsonify, g
from functools import wraps
from firebase_admin import auth
from bson import json_util
import json
from services.user_service import UserService
from services.artist_service import ArtistService
import logging

logger = logging.getLogger(__name__)


class UserController:

    def get_user_info(firebase_id):
       try:
           request_uid = getattr(g, "firebase_id", None)
           if not request_uid:
               return jsonify({"error": "Unauthorized"}), 401
           if request_uid != firebase_id:
               requester = Users.objects(firebase_id=request_uid).only("admin").first()
               if not requester or not requester.admin:
                   return jsonify({"error": "Forbidden"}), 403

           user = Users.objects(firebase_id=firebase_id).first()
           if user:
               return jsonify({
                   "status": "success",
                   "data": json.loads(user.to_json())
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
            request_uid = getattr(g, "firebase_id", None)
            if not request_uid:
                return jsonify({"error": "Unauthorized"}), 401
            if request_uid != firebase_id:
                requester = Users.objects(firebase_id=request_uid).only("admin").first()
                if not requester or not requester.admin:
                    return jsonify({"error": "Forbidden"}), 403

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
            # firebase uid from verified token only (set by @auth_required).
            uid = getattr(g, "firebase_id", None)
            if not uid:
                return jsonify({"error": "Unauthorized"}), 401

            # get email
            data = request.get_json()
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
        # Use Firebase UID from verified token only (set by @auth_required).
        firebase_uid = getattr(g, "firebase_id", None)
        if not firebase_uid:
            return jsonify({"error": "Unauthorized"}), 401

        data = request.get_json(silent=True) or {}
        logger.info(f"Creating user with data: {data}")
        try:
            if not data.get("name") or not data.get("email") or not data.get("tenant") or not data.get("followed_artist"):
                return jsonify({
                    "error": "Missing required fields"
                }), 400

            # Reject if client tries to register a different Firebase identity.
            incoming_firebase_id = data.get("firebaseId")
            if incoming_firebase_id and incoming_firebase_id != firebase_uid:
                return jsonify({"error": "Forbidden"}), 403

            # user already exists
            if Users.objects(firebase_id=firebase_uid).first():
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
                firebase_id = firebase_uid,
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
        data = request.get_json(silent=True) or {}
        logger.debug(f"Checking user exists: {data}")

        request_uid = getattr(g, "firebase_id", None)
        if not request_uid:
            return jsonify({"error": "Unauthorized"}), 401

        # Reject probing other users.
        requested_uid = data.get("firebase_id")
        if requested_uid and requested_uid != request_uid:
            return jsonify({"error": "Forbidden"}), 403

        firebase_uid = request_uid

        user = Users.objects(firebase_id=firebase_uid).first()

        if user:

            # print(user)
            return jsonify({
                "exists": True,
                "admin": user.admin,
                "is_premium": user.is_premium,
                "plan": user.plan,
                "expired_at": user.premium_expired_at
            }), 200
        else:
            # no user data in database yet
            return jsonify({
                "exists": False
            }), 200

    @staticmethod
    def check_is_admin():
        firebase_uid = getattr(g, "firebase_id", None)
        if not firebase_uid:
            return jsonify({"error": "Unauthorized"}), 401

        user = Users.objects(firebase_id=firebase_uid).first()
        if not user:
            return jsonify({"exists": False, "admin": False}), 404

        return jsonify({
            "exists": True,
            "admin": bool(user.admin)
        }), 200

    @staticmethod
    def get_all_tenant_company():
        """
        Get all companies name
        :return:
        """
        tenants = Tenant.objects().order_by("tenant_name")
        company = [
            {"tenant_name": t.tenant_name.lower(),
             "tenant_id": str(t.id) } for t in tenants]

        company.sort(key=lambda x: x["tenant_name"])

        return jsonify({
            "status": "success",
            "data": company
        }), 200

    @staticmethod
    def get_all_artist_by_tenant(tenant_id):
        try:
            artist_data = ArtistService.get_all_artists_by_tenant(tenant_id)

            return jsonify({
                "status": "success",
                "data": artist_data
            }), 200

        except Exception as e:
            return jsonify({
                "status": "error",
                "message": str(e)
            }), 500

    @staticmethod
    def get_me():
        firebase_id = getattr(g, "firebase_id", None)
        if not firebase_id:
            return jsonify({
                "error": "Unauthorized"
            }), 401

        user = Users.objects(firebase_id=firebase_id).first()
        if not user:
            return jsonify({
                "error": "User not found"
            }), 404

        # check for premium expiry & enforce artist limit
        UserService.enforce_artist_limit(user)

        user_data = UserService.get_me(firebase_id)
        return jsonify(user_data), 200

    @staticmethod
    def get_user_followed_artist():
        try:
            artist_data = UserService.get_followed_artist(g.firebase_id)

            return jsonify({
                "status": "success",
                "data": artist_data
            }), 200

        except ValueError as e:
            return jsonify({
                "status": "error",
                "message": str(e)
            }), 404

        except Exception as e:
            return jsonify({
                "status": "error",
                "message": str(e)
            }), 500

    @staticmethod
    def update_followed_artists():
        # 1. 使用統一的裝飾器獲取 firebase_id (g.firebase_id 已由 auth_required 設置)
        firebase_id = getattr(g, "firebase_id", None)
        if not firebase_id:
            return jsonify({"error": "Unauthorized"}), 401

        # Parse body
        data = request.get_json(silent=True) or {}
        artist_ids = data.get("artist_ids")

        if artist_ids is None:
            return jsonify({"error": "artist_ids is required"}), 400

        if not isinstance(artist_ids, list):
            return jsonify({"error": "artist_ids must be a list"}), 400

        result, error = UserService.update_followed_artists(
            firebase_id=firebase_id,
            artist_ids=artist_ids
        )

        if error:
            return jsonify({"error": error}), 400

        return jsonify({"data": result}), 200
