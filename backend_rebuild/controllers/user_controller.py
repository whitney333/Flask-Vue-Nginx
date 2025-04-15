from models.user_model import Users
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

    def get_by_firebase_id(firebase_id):
        """
        Get a user by Firebase ID
        :return:
        """
        try:
            # return QuerySet
            # use to_json() method to convert
            user = Users.objects(firebase_id__exact=firebase_id).first()

            if user:
                return {
                    "status": "success",
                    "data": user.to_dict()
                }, 200
            else:
                return {
                    "status": "err",
                    "message": "User not found"
                }, 404

        except Exception as e:
            return {
                "status": "err",
                "message": str(e)
            }, 500
    @staticmethod
    def create_user():
        """
        create new user
        :return: user object
        """
        # get data
        data = request.get_json()

        # TODO Check if user exists?
        try:
            firebase_id = data.get("firebase_id")
            name = data.get("name")
            company_name = data.get("company_name")
            artist_name = data.get("artist_name")
            image_url = data.get("image_url")
            email = data.get("email")

            new_user = Users(
                firebase_id = firebase_id,
                name = name,
                company_name = company_name,
                artist_name = artist_name,
                image_url = image_url,
                email = email,
            )
            new_user.save()
            return jsonify({
                "status": "success",
                "message": "User created successfully",
            }), 201
        except Exception as e:
            return jsonify({"err": str(e)}), 404

    @staticmethod
    def update_user():
        data = request.get_json()


