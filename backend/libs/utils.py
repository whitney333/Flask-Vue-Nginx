from models import user_db
from functools import wraps
from flask import request, jsonify
import firebase_admin
from firebase_admin import auth

def getIdFromFirebaseID(firebase_id):
    try:
        user = user_db.users.find_one({"firebaseId": firebase_id})
        if user:
            return user
        return None
    except Exception as e:
        print(f"Error getting user ID: {str(e)}")
        return None

def require_auth(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            auth_header = request.headers.get("Authorization")
            if not auth_header or not auth_header.startswith("Bearer "):
                return jsonify({"error": "Unauthorized"}), 401

            token = auth_header.split(" ")[1]
            
            try:
                # Verify the Firebase JWT
                decoded_token = auth.verify_id_token(token)
            except Exception as e:
                print(f"Error verifying token: {str(e)}")
                return jsonify({"error": "Invalid token"}), 401
            
            firebase_id = decoded_token['uid']
            user = getIdFromFirebaseID(firebase_id)
            
            if not user.user_id:
                return jsonify({"error": "User not found"}), 404
                
            # Add user_id to request context for later use
            request.user = user
            request.firebase_id = firebase_id
            
            return f(*args, **kwargs)
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    return decorated_function