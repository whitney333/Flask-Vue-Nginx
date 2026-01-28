from datetime import timedelta
from models.melon_model import Melon
from rules.music_chart import FOLLOWER_RANGE_RULES, RANGE_DAYS
from .artist_service import ArtistService
from .user_service import UserService


class MelonService:
    @staticmethod
    def get_chart_follower(user, artist_id, date_end, range_key):
        # ---------- check if user is premium or not ----------
        is_premium = UserService.is_active_premium(user)

        allowed_ranges = (
            FOLLOWER_RANGE_RULES["premium"]
            if is_premium
            else FOLLOWER_RANGE_RULES["free"]
        )

        if range_key not in allowed_ranges:
            return {
                "locked": True,
                "allowed_ranges": allowed_ranges
            }

        # ---------- calculate date ----------
        days = RANGE_DAYS[range_key]
        start_date = date_end - timedelta(days=days)

        # ----------get melon id ----------
        melon_id = ArtistService.get_melon_id(artist_id)
        # print("ml id: ", melon_id)

        records = (
            Melon.objects(
                melon_id=melon_id,
                datetime__gt=start_date,
                datetime__lte=date_end
            )
                .order_by("datetime")
                .only("datetime", "follower")
        )
        # ---------- format response ----------
        data = [
            {
                "datetime": r.datetime.strftime("%Y-%m-%d"),
                "follower": r.follower
            }
            for r in records
        ]

        return {
            "locked": False,
            "data": data,
            "meta": {
                "is_premium": is_premium,
                "range": range_key,
                "days": days,
                "allowed_ranges": allowed_ranges
            }
        }
