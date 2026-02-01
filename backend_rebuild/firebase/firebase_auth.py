import firebase_admin
from firebase_admin import auth, credentials

# Initialize Firebase Admin SDK (ensure you have your service account key)
# cred = credentials.Certificate('./firebase/venv/serviceAccountKey.json')
# firebase_admin.initialize_app(cred)

def verify_firebase_token(token):
    """
    Verify the Firebase ID token and return decoded data.
    """
    try:
        decoded_token = auth.verify_id_token(token)
        return decoded_token  # Contains user UID, email, etc.
    except Exception as e:
        print(f"[Firebase Auth] Token verification failed: {e}")
        return None
