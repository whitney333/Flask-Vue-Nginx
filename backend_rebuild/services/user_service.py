from models.user_model import Users

class UserService:

    @staticmethod
    def get_me(firebase_id: str):
        user = Users.objects(firebase_id=firebase_id).first()
        if not user:
            return None

        return {
            "firebase_id": user.firebase_id,
            "email": user.email,
            "name": user.name,
            "photo": user.image_url,
            "tenant": str(user.tenant.id) if user.tenant else None,

            "admin": user.admin,
            "created_at": user.created_at,
            "last_login_at": user.last_login_at,

            # ===== subscription =====
            "is_premium": user.is_premium,
            "plan": user.plan,
            "premium_expired_at": user.premium_expired_at,

            # ===== artists =====
            "followed_artists": [
                {
                    "artist_id": str(a.id),
                    "english_name": a.english_name,
                    "korean_name": a.korean_name,
                    "image": a.image_url
                }
                for a in (user.followed_artist or [])
            ]
        }