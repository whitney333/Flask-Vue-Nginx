from flask import request, jsonify
from functools import wraps
from firebase.firebase_auth import verify_firebase_token

def getIdFromFirebaseID(firebase_id):
    try:
        data = user_db.users.find_one({"firebaseId": firebase_id})
        return data["_id"]
    except Exception as e:
        return str(e)

def requires_auth(f):
    """Decorator to require Firebase authentication for routes."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return jsonify({"error": "Unauthorized"}), 401

        token = auth_header.split(" ")[1]
        decoded_token = verify_firebase_token(token)

        if not decoded_token:
            return jsonify({"error": "Invalid token"}), 401
        
        # Add the firebase ID and user ID to kwargs
        kwargs['firebase_id'] = decoded_token['uid']
        kwargs['user_id'] = getIdFromFirebaseID(decoded_token['uid'])
        
        return f(*args, **kwargs)
    return decorated_function