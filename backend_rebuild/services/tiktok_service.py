from datetime import timedelta
from models.sns.tiktok_model import Tiktok


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
