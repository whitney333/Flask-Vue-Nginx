from datetime import timedelta
from chart_rules.bilibili_chart_rules import FOLLOWER_RANGE_RULES, RANGE_DAYS
from models.sns.bilibili_model import Bilibili
from .artist_service import ArtistService


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
    def get_follower(user, artist_id, date_end, range_key):
        pass