from flask import request, jsonify, g
from functools import wraps
from firebase.firebase_auth import verify_firebase_token
from firebase_admin import auth
from models.user_model import Users


def getIdFromFirebaseID(firebase_id):
    try:
        user = Users.find_one({"firebase_id": firebase_id})
        return user.id if user else None
    except Exception as e:
        return str(e)

# def requires_auth(f):
#     """
#     Decorator to require Firebase authentication for routes.
#     """
#
#     @wraps(f)
#     def decorated_function(*args, **kwargs):
#         auth_header = request.headers.get("Authorization")
#         if not auth_header or not auth_header.startswith("Bearer "):
#             return jsonify({"error": "Unauthorized"}), 401
#
#         token = auth_header.split(" ")[1]
#         decoded_token = verify_firebase_token(token)
#
#         if not decoded_token:
#             return jsonify({"error": "Invalid token"}), 401
#
#         # Add the firebase ID and user ID to kwargs
#         kwargs['firebase_id'] = decoded_token['uid']
#         kwargs['user_id'] = getIdFromFirebaseID(decoded_token['uid'])
#
#         return f(*args, **kwargs)
#
#     return decorated_function

# wrap up firebase token required
def auth_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return jsonify({"error": "Unauthorized"}), 401

        token = auth_header.split(" ")[1]

        try:
            decoded_token = verify_firebase_token(token)
        except Exception as e:
            return jsonify({"error": f"Invalid token: {str(e)}"}), 401

        # store firebase_id in global
        g.firebase_id = decoded_token["uid"]
        g.user_id = getIdFromFirebaseID(decoded_token["uid"])
        return f(*args, **kwargs)
    return wrapper
