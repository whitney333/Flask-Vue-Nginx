'''
updated: 2025-08-04
user controller
- get user by firebase id (/v1/auth/firebase/<string:firebase_id>) -> GET
    - args:
        - firebase_id: string
    - return: user object
    - error:
        - 400: bad request
        - 404: user not found
        - 500: internal server error
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
        - 404: tenant not found
        - 404: artist not found
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
        - 404: user not found
        - 500: internal server error
'''

from models.user_model import User
import datetime
from mongoengine import ValidationError, DoesNotExist
from flask import request, jsonify
import uuid
from functools import wraps
from firebase_admin import auth


# wrap up firebase token required
def auth_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not request.headers.get('Authorization'):
            return jsonify({'error': 'No token provided'}), 401

        try:
            token = request.headers['Authorization'].split(' ').pop()
            decoded_token = auth.verify_id_token(token)
            request.user = decoded_token
        except Exception as e:
            return jsonify({'error': f'Invalid token: {str(e)}'}), 401

        return f(*args, **kwargs)

    return wrapper

class UserController:

    def get_user_by_firebase_id(firebase_id):
        try:
            # return QuerySet
            # use to_json() method to convert
            user = User.objects(firebase_id__exact=firebase_id).first()

            if user:
                return {
                    "status": "success",
                    "data": user.to_dict()
                }, 200
            else:
                return jsonify({"error": "User not found"}), 404

        except Exception as e:
            return jsonify({"error": str(e)}), 500

    
    def create_user():
        # get data
        data = request.get_json()

        try:
            if not data.get("firebase_id") or not data.get("name") or not data.get("image_url") or not data.get("email") or not data.get("tenant_id") or not data.get("followed_artist"):
                return jsonify({"error": "Missing required fields"}), 400

            if User.objects(firebase_id=data.get("firebase_id")).first():
                return jsonify({"error": "User already exists"}), 400

            tenant_id = data.get("tenant_id")
            tenant = Tenant.objects(id=tenant_id).first()
            if not tenant:
                return jsonify({"error": "Tenant not found"}), 404
            
            artist_ids = data.get("followed_artist")
            if not artist_ids:
                return jsonify({"error": "Followed artist is required"}), 400
            
            artists = Artist.objects(id__in=artist_ids)
            if not artists or artists.count() != len(artist_ids):
                return jsonify({"error": "Artist not found"}), 404
            
        
            new_user = User(
                firebase_id = data.get("firebase_id"),
                name = data.get("name"),
                image_url = data.get("image_url"),
                email = data.get("email"),
                tenant = tenant,
                followed_artist = artists,
                admin = False,
            )
            new_user.save()
            return jsonify({
                "status": "success",
                "message": "User created successfully",
                "data": new_user.to_json(),
            }), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    def update_user(user_id):
        data = request.get_json()
        try:
            user = User.objects(id=user_id).first()
            if user:
                user.update(**data)
                user.save()
                return jsonify({
                    "status": "success",
                    "message": "User updated successfully",
                }), 200
            else:
                return jsonify({"error": "User not found"}), 404
        except Exception as e:
            return jsonify({"error": str(e)}), 500


