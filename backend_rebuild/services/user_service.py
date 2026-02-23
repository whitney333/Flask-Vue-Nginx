from models.user_model import Users
from models.artist_model import Artists
from datetime import datetime, timezone

class UserService:
    PLAN_ARTIST_LIMIT = {
        "free": 1,
        "starter": 1,
        "standard": 10,
    }

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
            "billing_interval": user.billing_interval,
            # ===== artist limit =====
            "artist_limit": UserService.PLAN_ARTIST_LIMIT.get(user.plan, 1),

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
                set__billing_interval=None,
                set__stripe_subscription_id=None,
                set__premium_expired_at=None
            )
            return False

    @staticmethod
    def get_followed_artist(firebase_id):
        """
        return list of followed artists (dict)
        raise ValueError if no user or no followed artists
        """

        user = Users.objects(firebase_id=firebase_id).first()

        if not user or not user.followed_artist:
            raise ValueError("No followed artists")

        artist_data = []
        for artist in user.followed_artist:
            artist_data.append({
                "id": str(artist.id) if artist.id else None,
                "artist_id": artist.artist_id,
                "english_name": artist.english_name,
                "korean_name": artist.korean_name,
                "image": artist.image_url
            })

        return artist_data

    @staticmethod
    def update_followed_artists(firebase_id, artist_ids):
        user = Users.objects(firebase_id=firebase_id).first()
        if not user:
            return None, "User not found"

        # check plan
        active_premium = UserService.is_active_premium(user)
        plan = user.plan if active_premium else "free"
        artist_limit = UserService.PLAN_ARTIST_LIMIT.get(plan, 1)

        # check limit
        if len(artist_ids) > artist_limit:
            return None, f"Your current plan allows up to {artist_limit} artist(s)."

        # check if Artist exists
        artists = Artists.objects(id__in=artist_ids)
        if len(artists) != len(artist_ids):
            return None, "Some artists not found"

        # update user
        user.update(set__followed_artist=artists)

        return {
                   "followed_artist_count": len(artists),
                   "artist_limit": artist_limit,
                   "followed_artists": [
                       {
                           "artist_id": str(a.id),
                           "english_name": a.english_name,
                           "korean_name": a.korean_name,
                           "image": a.image_url
                       }
                       for a in artists
                   ]
               }, None
