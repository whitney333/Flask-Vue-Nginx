from models.user_model import Users
from datetime import datetime, timezone

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

    @staticmethod
    def is_active_premium(user):
        """
        check if user is valid premium.
        1. user.is_premium must be: True
        2. premium_expired_at must exist and >= now
        3. if premium expired, downgrade
        :param user:
        :return:
        """
        if not user or not user.is_premium:
            return False

        if not user.premium_expired_at:
            return False

        expired_at = user.premium_expired_at

        if expired_at.tzinfo is None:
            expired_at = expired_at.replace(tzinfo=timezone.utc)

        now = datetime.now(timezone.utc)
        if now <= expired_at:
            return True
        else:
            # downgrade user
            user.update(
                set__is_premium=False,
                set__plan="free",
                set__stripe_subscription_id=None,
                set__premium_expired_at=None
            )
            return False
