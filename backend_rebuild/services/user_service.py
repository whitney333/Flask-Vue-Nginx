from models.user_model import Users
from models.artist_model import Artists
from datetime import datetime, timezone
from bson import ObjectId
from mongoengine import Q
import logging

logger = logging.getLogger(__name__)

class UserService:
    PLAN_ARTIST_LIMIT = {
        "free": 1,
        "starter": 5,
        "standard": 20,
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
    def enforce_artist_limit(user):
        """
        Slice the followed_artist list to match the user's plan limit.
        """
        # check active premium status for current plan
        active_premium = UserService.is_active_premium(user)
        plan = user.plan if active_premium else "free"
        limit = UserService.PLAN_ARTIST_LIMIT.get(plan, 1)

        if len(user.followed_artist) > limit:
            # slice the list to the first 'limit' items
            user.followed_artist = user.followed_artist[:limit]
            user.save()
            logger.info(f"[UserService] Plan {plan} limit enforcement: sliced artists to {limit} for {user.firebase_id}")

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
        if not user:
            return False

        if not user.is_premium:
            # 如果標記為非 premium，但仍有未處理的過期時間（防禦性檢查）
            return False

        if not user.premium_expired_at:
            # 如果是 premium 但沒過期時間，可能是手動設置或異常
            return True

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

            # reload user to get latest state for limit enforcement
            user.reload()
            UserService.enforce_artist_limit(user)
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

        normalized_artist_ids = []
        seen_artist_ids = set()
        for artist_id in artist_ids:
            normalized_artist_id = str(artist_id).strip() if artist_id is not None else ""
            if normalized_artist_id and normalized_artist_id not in seen_artist_ids:
                normalized_artist_ids.append(normalized_artist_id)
                seen_artist_ids.add(normalized_artist_id)

        if not normalized_artist_ids:
            return None, "artist_ids must include at least one artist"

        active_premium = UserService.is_active_premium(user)
        plan = user.plan if active_premium else "free"
        artist_limit = UserService.PLAN_ARTIST_LIMIT.get(plan, 1)

        object_id_candidates = [
            artist_id
            for artist_id in normalized_artist_ids
            if ObjectId.is_valid(artist_id)
        ]
        query = Q(artist_id__in=normalized_artist_ids)
        if object_id_candidates:
            query = query | Q(id__in=object_id_candidates)

        artists = list(Artists.objects(query))
        artists_by_lookup_id = {}
        for artist in artists:
            artists_by_lookup_id[str(artist.id)] = artist
            artists_by_lookup_id[str(artist.artist_id)] = artist

        resolved_artists = []
        resolved_artist_ids = set()
        for artist_id in normalized_artist_ids:
            artist = artists_by_lookup_id.get(artist_id)
            if not artist:
                return None, "Some artists not found"

            resolved_artist_id = str(artist.id)
            if resolved_artist_id not in resolved_artist_ids:
                resolved_artists.append(artist)
                resolved_artist_ids.add(resolved_artist_id)

        locked_artist = None
        current_followed_artists = user.followed_artist or []
        if current_followed_artists:
            locked_artist = next(
                (
                    artist
                    for artist in current_followed_artists
                    if user.tenant and artist.tenant_id and str(artist.tenant_id.id) == str(user.tenant.id)
                ),
                current_followed_artists[0]
            )

        if locked_artist and str(locked_artist.id) not in resolved_artist_ids:
            return None, "Locked artist cannot be removed"

        if not user.tenant or not any(str(artist.tenant_id.id) == str(user.tenant.id) for artist in resolved_artists if artist.tenant_id):
            return None, "Must follow at least 1 artist from your own company"

        # 2. 檢查輸入的清單是否超過目前方案限額
        if len(resolved_artists) > artist_limit:
            return None, f"Your current plan allows up to {artist_limit} artist(s)."

        # 4. 更新用戶資料
        user.followed_artist = resolved_artists
        user.save()

        # 5. 再次主動執行限額校驗（作為最後防護機制）
        UserService.enforce_artist_limit(user)
        user.reload() # 獲取校驗後的最終狀態

        # 重新計算最終的藝人清單與數量
        final_artists = user.followed_artist or []
        
        return {
                   "followed_artist_count": len(final_artists),
                   "artist_limit": artist_limit,
                   "followed_artists": [
                       {
                           "artist_id": str(a.id),
                           "english_name": a.english_name,
                           "korean_name": a.korean_name,
                           "image": a.image_url
                       }
                       for a in final_artists
                   ]
               }, None
