from datetime import timedelta
from models.sns.tiktok_model import Tiktok
from rules.tiktok_chart import FOLLOWER_RANGE_RULES, RANGE_DAYS
from .artist_service import ArtistService



def to_int(value, default=0):
    try:
        return int(value)
    except (TypeError, ValueError):
        return default

class TiktokService:

    @staticmethod
    def get_follower_growth(tiktok_id, campaign_start):
        """
        Get Tiktok follower growth for a campaign
        (campaign_start -14d) → (campaign_start +14d)
        :param tiktok_id:
        :param campaign_start:
        :return:
        """
        before_target = campaign_start - timedelta(days=14)
        after_target = campaign_start + timedelta(days=14)

        # find the latest record before the campaign start
        before_record = (
            Tiktok.objects(
                tiktok_id=tiktok_id,
                datetime__lte=before_target
            )
            .order_by("-datetime")
            .first()
        )

        # find the latest record after the campaign
        after_record = (
            Tiktok.objects(
                tiktok_id=tiktok_id,
                datetime__lte=after_target
            )
            .order_by("-datetime")
            .first()
        )
        # if not enough data, return None
        if before_record is None or after_record is None:
            return None

        before = to_int(before_record.follower)
        after = to_int(after_record.follower)

        growth_percentage = (
            round(((after - before) / before) * 100, 2)
            if before > 0 else 0
        )

        return {
            "before": {
                "date": before_record.datetime.isoformat(),
                "follower": to_int(before_record.follower)
            },
            "after": {
                "date": after_record.datetime.isoformat(),
                "follower": to_int(after_record.follower)
            },
            "growth": after - before,
            "percentage": growth_percentage
        }

    @staticmethod
    def get_hashtag_growth(tiktok_id, campaign_start):
        """
        Get Tiktok follower growth for a campaign
        (campaign_start -14d) → (campaign_start +14d)
        :param tiktok_id:
        :param campaign_start:
        :return:
        """
        before_target = campaign_start - timedelta(days=14)
        after_target = campaign_start + timedelta(days=14)

        # find the latest record before the campaign start
        before_record = (
            Tiktok.objects(
                tiktok_id=tiktok_id,
                datetime__lte=before_target
            )
            .order_by("-datetime")
            .first()
        )

        # find the latest record after the campaign
        after_record = (
            Tiktok.objects(
                tiktok_id=tiktok_id,
                datetime__lte=after_target
            )
            .order_by("-datetime")
            .first()
        )
        # if not enough data, return None
        if before_record is None or after_record is None:
            return None

        before = to_int(before_record.hashtag)
        after = to_int(after_record.hashtag)

        growth_percentage = (
            round(((after - before) / before) * 100, 2)
            if before > 0 else 0
        )

        return {
            "before": {
                "date": before_record.datetime.isoformat(),
                "hashtag": to_int(before_record.hashtag)
            },
            "after": {
                "date": after_record.datetime.isoformat(),
                "hashtag": to_int(after_record.hashtag)
            },
            "growth": after - before,
            "percentage": growth_percentage
        }

    @staticmethod
    def get_chart_follower(user, artist_id, date_end, range_key):
        # ---------- check if user is premium or not ----------
        is_premium = bool(user and user.is_premium)

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

        # ----------get tiktok id ----------
        tiktok_id = ArtistService.get_tiktok_id(artist_id)
        # print("tk id: ", tiktok_id)

        records = (
            Tiktok.objects(
                tiktok_id=tiktok_id,
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
                "follower": to_int(r.follower)
            }
            for r in records
        ]

        return {
            "locked": False,
            "data": data,
            "meta": {
                "is_premium": is_premium,
                "range": range_key,
                "days": days
            }
        }

    @staticmethod
    def get_chart_like(user, artist_id, date_end, range_key):
        # ---------- check if user is premium or not ----------
        is_premium = bool(user and user.is_premium)

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

        # ----------get tiktok id ----------
        tiktok_id = ArtistService.get_tiktok_id(artist_id)
        # print("tk id: ", tiktok_id)

        records = (
            Tiktok.objects(
                tiktok_id=tiktok_id,
                datetime__gt=start_date,
                datetime__lte=date_end
            )
                .order_by("datetime")
                .only("datetime", "like")
        )
        # ---------- format response ----------
        data = [
            {
                "datetime": r.datetime.strftime("%Y-%m-%d"),
                "like": to_int(r.like)
            }
            for r in records
        ]

        return {
            "locked": False,
            "data": data,
            "meta": {
                "is_premium": is_premium,
                "range": range_key,
                "days": days
            }
        }

    @staticmethod
    def get_chart_hashtag(user, artist_id, date_end, range_key):
        # ---------- check if user is premium or not ----------
        is_premium = bool(user and user.is_premium)

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

        # ----------get tiktok id ----------
        tiktok_id = ArtistService.get_tiktok_id(artist_id)
        # print("tk id: ", tiktok_id)

        records = (
            Tiktok.objects(
                tiktok_id=tiktok_id,
                datetime__gt=start_date,
                datetime__lte=date_end
            )
                .order_by("datetime")
                .only("datetime", "hashtag")
        )
        # ---------- format response ----------
        data = [
            {
                "datetime": r.datetime.strftime("%Y-%m-%d"),
                "hashtag": to_int(r.hashtag)
            }
            for r in records
        ]

        return {
            "locked": False,
            "data": data,
            "meta": {
                "is_premium": is_premium,
                "range": range_key,
                "days": days
            }
        }
