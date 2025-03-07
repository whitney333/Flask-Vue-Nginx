from models import user_db

def getIdFromFirebaseID(firebase_id):
    try:
        data = user_db.users.find_one({"firebaseId": firebase_id})
        return data["_id"]
    except Exception as e:
        return str(e)
