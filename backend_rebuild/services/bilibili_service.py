from datetime import timedelta
from models.sns.bilibili_model import Bilibili
from rules.bilibili_chart import FOLLOWER_RANGE_RULES, RANGE_DAYS
from .artist_service import ArtistService
from collections import defaultdict


def to_int(value, default=0):
    try:
        return int(value)
    except (TypeError, ValueError):
        return default

class BilibiliService:
    @staticmethod
    def get_follower_growth(bilibili_id, campaign_start):
        """
            Get Bilibili follower growth for a campaign
            (campaign_start -14d) → (campaign_start +14d)
            :param bilibili_id:
            :param campaign_start:
            :return:
        """
        before_target = campaign_start - timedelta(days=14)
        after_target = campaign_start + timedelta(days=14)

        # find the latest record before the campaign start
        before_record = (
            Bilibili.objects(
                user_id=bilibili_id,
                datetime__lte=before_target
            )
                .order_by("-datetime")
                .first()
        )

        # find the latest record after the campaign
        after_record = (
            Bilibili.objects(
                user_id=bilibili_id,
                datetime__lte=after_target
            )
                .order_by("-datetime")
                .first()
        )

        # if not enough data, return None
        if before_record is None or after_record is None:
            return None

        before = before_record.follower
        after = after_record.follower

        growth_percentage = (
            round(((after - before) / before) * 100, 2)
            if before > 0 else 0
        )

        return {
            "before": {
                "date": before_record.datetime.isoformat(),
                "follower": before_record.follower
            },
            "after": {
                "date": after_record.datetime.isoformat(),
                "follower": after_record.follower
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

        # ----------get bilibili id ----------
        bilibili_id = ArtistService.get_bilibili_id(artist_id)

        records = (
            Bilibili.objects(
                user_id=bilibili_id,
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
                "follower": to_int(r.follower),
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

    @staticmethod
    def get_chart_view(user, artist_id, date_end, range_key):
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

        # ----------get bilibili id ----------
        bilibili_id = ArtistService.get_bilibili_id(artist_id)

        # query
        records = (
            Bilibili.objects(
                user_id=bilibili_id,
                datetime__gt=start_date,
                datetime__lte=date_end
            )
                .order_by("datetime")
                .only("user_id", "datetime", "data")
        )

        if not records:
            return []

        # aggregate in python
        bucket = defaultdict(lambda: {
            "count": 0,
            "total_view": 0
        })

        for doc in records:
            day_key = doc.datetime.strftime("%Y-%m-%d")

            for item in (doc.data or []):
                bucket[day_key]["count"] += 1
                bucket[day_key]["total_view"] += int(item.view or 0)

        # ---------- build result ----------
        result = []
        for day, v in sorted(bucket.items()):
            count = v["count"]
            total_view = v["total_view"]

            result.append({
                "datetime": day,
                "bilibili_id": bilibili_id,
                "total_view": total_view,
                "avg_view": (total_view / count) if count > 0 else 0
            })

        return {
            "locked": False,
            "data": result,
            "meta": {
                "is_premium": is_premium,
                "range": range_key,
                "days": days,
                "allowed_ranges": allowed_ranges
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

        # ----------get bilibili id ----------
        bilibili_id = ArtistService.get_bilibili_id(artist_id)

        # query
        records = (
            Bilibili.objects(
                user_id=bilibili_id,
                datetime__gt=start_date,
                datetime__lte=date_end
            )
                .order_by("datetime")
                .only("user_id", "datetime", "data")
        )

        if not records:
            return []

        # aggregate in python
        bucket = defaultdict(lambda: {
            "count": 0,
            "total_like": 0
        })

        for doc in records:
            day_key = doc.datetime.strftime("%Y-%m-%d")

            for item in (doc.data or []):
                bucket[day_key]["count"] += 1
                bucket[day_key]["total_like"] += int(item.like or 0)

        # ---------- build result ----------
        result = []
        for day, v in sorted(bucket.items()):
            count = v["count"]
            total_like = v["total_like"]

            result.append({
                "datetime": day,
                "bilibili_id": bilibili_id,
                "total_like": total_like,
                "avg_like": (total_like / count) if count > 0 else 0
            })

        return {
            "locked": False,
            "data": result,
            "meta": {
                "is_premium": is_premium,
                "range": range_key,
                "days": days,
                "allowed_ranges": allowed_ranges
            }
        }

    @staticmethod
    def get_chart_comment(user, artist_id, date_end, range_key):
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

        # ----------get bilibili id ----------
        bilibili_id = ArtistService.get_bilibili_id(artist_id)

        # query
        records = (
            Bilibili.objects(
                user_id=bilibili_id,
                datetime__gt=start_date,
                datetime__lte=date_end
            )
                .order_by("datetime")
                .only("user_id", "datetime", "data")
        )

        if not records:
            return []

        # aggregate in python
        bucket = defaultdict(lambda: {
            "count": 0,
            "total_comment": 0
        })

        for doc in records:
            day_key = doc.datetime.strftime("%Y-%m-%d")

            for item in (doc.data or []):
                bucket[day_key]["count"] += 1
                bucket[day_key]["total_comment"] += int(item.comment or 0)

        # ---------- build result ----------
        result = []
        for day, v in sorted(bucket.items()):
            count = v["count"]
            total_comment = v["total_comment"]

            result.append({
                "datetime": day,
                "bilibili_id": bilibili_id,
                "total_comment": total_comment,
                "avg_comment": (total_comment / count) if count > 0 else 0
            })

        return {
            "locked": False,
            "data": result,
            "meta": {
                "is_premium": is_premium,
                "range": range_key,
                "days": days,
                "allowed_ranges": allowed_ranges
            }
        }

    @staticmethod
    def get_chart_share(user, artist_id, date_end, range_key):
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

        # ----------get bilibili id ----------
        bilibili_id = ArtistService.get_bilibili_id(artist_id)

        # query
        records = (
            Bilibili.objects(
                user_id=bilibili_id,
                datetime__gt=start_date,
                datetime__lte=date_end
            )
                .order_by("datetime")
                .only("user_id", "datetime", "data")
        )

        if not records:
            return []

        # aggregate in python
        bucket = defaultdict(lambda: {
            "count": 0,
            "total_share": 0
        })

        for doc in records:
            day_key = doc.datetime.strftime("%Y-%m-%d")

            for item in (doc.data or []):
                bucket[day_key]["count"] += 1
                bucket[day_key]["total_share"] += int(item.share or 0)

        # ---------- build result ----------
        result = []
        for day, v in sorted(bucket.items()):
            count = v["count"]
            total_share = v["total_share"]

            result.append({
                "datetime": day,
                "bilibili_id": bilibili_id,
                "total_share": total_share,
                "avg_share": (total_share / count) if count > 0 else 0
            })

        return {
            "locked": False,
            "data": result,
            "meta": {
                "is_premium": is_premium,
                "range": range_key,
                "days": days,
                "allowed_ranges": allowed_ranges
            }
        }

    @staticmethod
    def get_chart_danmu(user, artist_id, date_end, range_key):
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

        # ----------get bilibili id ----------
        bilibili_id = ArtistService.get_bilibili_id(artist_id)

        # query
        records = (
            Bilibili.objects(
                user_id=bilibili_id,
                datetime__gt=start_date,
                datetime__lte=date_end
            )
                .order_by("datetime")
                .only("user_id", "datetime", "data")
        )

        if not records:
            return []

        # aggregate in python
        bucket = defaultdict(lambda: {
            "count": 0,
            "total_danmu": 0
        })

        for doc in records:
            day_key = doc.datetime.strftime("%Y-%m-%d")

            for item in (doc.data or []):
                bucket[day_key]["count"] += 1
                bucket[day_key]["total_danmu"] += int(item.danmu or 0)

        # ---------- build result ----------
        result = []
        for day, v in sorted(bucket.items()):
            count = v["count"]
            total_danmu = v["total_danmu"]

            result.append({
                "datetime": day,
                "bilibili_id": bilibili_id,
                "total_danmu": total_danmu,
                "avg_danmu": (total_danmu / count) if count > 0 else 0
            })

        return {
            "locked": False,
            "data": result,
            "meta": {
                "is_premium": is_premium,
                "range": range_key,
                "days": days,
                "allowed_ranges": allowed_ranges
            }
        }

    @staticmethod
    def get_chart_coin(user, artist_id, date_end, range_key):
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

        # ----------get bilibili id ----------
        bilibili_id = ArtistService.get_bilibili_id(artist_id)

        # query
        records = (
            Bilibili.objects(
                user_id=bilibili_id,
                datetime__gt=start_date,
                datetime__lte=date_end
            )
                .order_by("datetime")
                .only("user_id", "datetime", "data")
        )

        if not records:
            return []

        # aggregate in python
        bucket = defaultdict(lambda: {
            "count": 0,
            "total_coin": 0
        })

        for doc in records:
            day_key = doc.datetime.strftime("%Y-%m-%d")

            for item in (doc.data or []):
                bucket[day_key]["count"] += 1
                bucket[day_key]["total_coin"] += int(item.coin or 0)

        # ---------- build result ----------
        result = []
        for day, v in sorted(bucket.items()):
            count = v["count"]
            total_coin = v["total_coin"]

            result.append({
                "datetime": day,
                "bilibili_id": bilibili_id,
                "total_coin": total_coin,
                "avg_coin": (total_coin / count) if count > 0 else 0
            })

        return {
            "locked": False,
            "data": result,
            "meta": {
                "is_premium": is_premium,
                "range": range_key,
                "days": days,
                "allowed_ranges": allowed_ranges
            }
        }

    @staticmethod
    def get_chart_collect(user, artist_id, date_end, range_key):
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

        # ----------get bilibili id ----------
        bilibili_id = ArtistService.get_bilibili_id(artist_id)

        # query
        records = (
            Bilibili.objects(
                user_id=bilibili_id,
                datetime__gt=start_date,
                datetime__lte=date_end
            )
                .order_by("datetime")
                .only("user_id", "datetime", "data")
        )

        if not records:
            return []

        # aggregate in python
        bucket = defaultdict(lambda: {
            "count": 0,
            "total_collect": 0
        })

        for doc in records:
            day_key = doc.datetime.strftime("%Y-%m-%d")

            for item in (doc.data or []):
                bucket[day_key]["count"] += 1
                bucket[day_key]["total_collect"] += int(item.collect or 0)

        # ---------- build result ----------
        result = []
        for day, v in sorted(bucket.items()):
            count = v["count"]
            total_collect = v["total_collect"]

            result.append({
                "datetime": day,
                "bilibili_id": bilibili_id,
                "total_collect": total_collect,
                "avg_collect": (total_collect / count) if count > 0 else 0
            })

        return {
            "locked": False,
            "data": result,
            "meta": {
                "is_premium": is_premium,
                "range": range_key,
                "days": days,
                "allowed_ranges": allowed_ranges
            }
        }

    @staticmethod
    def get_chart_engagement_rate(user, artist_id, date_end, range_key):
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

        # ----------get bilibili id ----------
        bilibili_id = ArtistService.get_bilibili_id(artist_id)

        # query
        records = (
            Bilibili.objects(
                user_id=bilibili_id,
                datetime__gt=start_date,
                datetime__lte=date_end
            )
                .order_by("datetime")
                .only("datetime", "data")
        )

        if not records:
            return []

        bucket = defaultdict(lambda: {
            "total_view": 0,
            "total_like": 0,
            "total_comment": 0,
            "total_share": 0,
            "total_collect": 0,
            "total_coin": 0,
            "total_danmu": 0,
        })

        # ---------- unwind + group ----------
        for doc in records:
            day_key = doc.datetime.strftime("%Y-%m-%d")

            for post in (doc.data or []):
                bucket[day_key]["total_view"] += int(post.view or 0)
                bucket[day_key]["total_like"] += int(post.like or 0)
                bucket[day_key]["total_comment"] += int(post.comment or 0)
                bucket[day_key]["total_share"] += int(post.share or 0)
                bucket[day_key]["total_collect"] += int(post.collect or 0)
                bucket[day_key]["total_coin"] += int(post.coin or 0)
                bucket[day_key]["total_danmu"] += int(post.danmu or 0)

        # ---------- build result ----------
        result = []

        for day, v in sorted(bucket.items()):
            total_view = v["total_view"]

            engagement = (
                    v["total_like"]
                    + v["total_comment"]
                    + v["total_share"]
                    + v["total_collect"]
                    + v["total_coin"]
                    + v["total_danmu"]
            )

            engagement_rate = (
                engagement / total_view if total_view > 0 else 0
            )

            result.append({
                "datetime": day,
                "engagement_rate": engagement_rate
            })

        return {
            "locked": False,
            "data": result,
            "meta": {
                "is_premium": is_premium,
                "range": range_key,
                "days": days,
                "allowed_ranges": allowed_ranges
            }
        }
