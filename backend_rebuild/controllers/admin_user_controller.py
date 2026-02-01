from models.tenant_model import Tenant
from models.user_model import Users
from models.artist_model import Artists
from flask import jsonify, request
from datetime import datetime, timezone
from firebase_admin import auth
from mongoengine.errors import ValidationError
from bson import ObjectId
import re
import os
import uuid
import boto3
from dotenv import load_dotenv
import traceback


class AdminUserController:
    def __init__(self, admin):
        self.admin = admin

    @classmethod
    def getAllUsers(cls):
        """
        get all users
        :return:
        """
        try:
            tenant = request.args.get("tenant")
            name = request.args.get("name")
            admin = request.args.get("admin")
            email = request.args.get("email")
            created_at = request.args.get("created_at")
            followed_artist = request.args.get("followed_artist")
            image_url = request.args.get("image_url")

            sort_field = request.args.get("sort", "created_at")
            order = request.args.get("order", "asc")

            page = int(request.args.get("page", 1))
            limit = int(request.args.get("limit", 10))

            # Query building
            query = {}
            if tenant:
                query["tenant"] = tenant
            if name:
                query["name__icontains"] = name
            if email:
                query["email__iexact"] = email
            if admin:
                query["admin__iexact"] = admin

            users_query = Users.objects(**query)

            if order == "desc":
                users_query = users_query.order_by(f"-{sort_field}")
            else:
                users_query = users_query.order_by(sort_field)

            # pagination
            total = users_query.count()
            users = users_query.skip((page - 1) * limit).limit(limit)

            result = []
            for u in users:
                result.append({
                    "tenant": str(u.tenant.tenant_name) if u.tenant else None,
                    "user_id": str(u.id) if u.id else None,
                    "name": u.name,
                    "firebase_id": u.firebase_id,
                    "admin": u.admin,
                    "email": u.email,
                    "created_at": u.created_at,
                    "followed_artist": [{
                        "id": str(a.id),
                        "korean_name": a.korean_name,
                        "english_name": a.english_name
                    } for a in u.followed_artist],
                    "image": u.image_url
                })

            return jsonify({
                "message": "success",
                "total": total,
                "page": page,
                "limit": limit,
                "count": len(result),
                "data": result
            }), 200
        except Exception as e:
            return jsonify({
                "error": str(e)
            }), 500

    @classmethod
    def getSingleUser(cls, user_id):
        """
        get single user's info
        :param user_id:
        :return:
        """
        try:
            user = Users.objects(id=user_id).first()
            if not user:
                return jsonify({
                    "error": "User not found"
                }), 404

            result = {
                "tenant": str(user.tenant.tenant_name) if user.tenant else None,
                "user_id": str(user.id) if user.id else None,
                "name": user.name,
                "firebase_id": user.firebase_id,
                "admin": user.admin,
                "email": user.email,
                "followed_artist": [{
                    "id": str(a.id),
                    "korean_name": a.korean_name,
                    "english_name": a.english_name
                } for a in user.followed_artist],
                "image": user.image_url
            }

            return jsonify({
                "message": "success",
                "data": result
            }), 200
        except Exception as e:
            return jsonify({
                "error": str(e)
            }), 500

    @classmethod
    def addUser(cls):
        """
        add user in firebase and database
        :return:
        """
        try:
            data = request.get_json()
            email = data.get("email")
            name = data.get("name")
            tenant = data.get("tenant")
            admin = data.get("admin", False)
            followed_artist = data.get("followed_artist")

            if not email or not tenant:
                return jsonify({
                    "message": "email and tenant are required"
                }), 400

            # check if email is duplicated


            # create firebase auth user
            # firebase_user = auth.create_user(
            #     email=email,
            #
            # )
            # generate reset password link

            # send invite email

            # create user profile in mongodb

            return jsonify({
                "message": "User created successfully",
                "data": data
            }), 201
        except Exception as e:
            return jsonify({
                "error": str(e)
            }), 500

    @classmethod
    def updateUser(cls, user_id):
        pass

    @classmethod
    def cancelUser(cls, user_id):
        """
        cancel user
        :param user_id:
        :return:
        """
        pass
