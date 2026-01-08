from datetime import datetime, timedelta
from models.sns.weibo_model import Weibo

class WeiboService:

    @staticmethod
    def get_follower_growth(weibo_id, campaign_start):
        """
        Get Weibo follower growth for a campaign
        (campaign_start -14d) → (campaign_start +14d)
        :param weibo_id:
        :param campaign_start:
        :return:
        """
        before_target = campaign_start - timedelta(days=14)
        after_target = campaign_start + timedelta(days=14)

        # find the latest record before the campaign start
        before_record = (
            Weibo.objects(
                weibo_id=weibo_id,
                datetime__lte=before_target
            )
            .order_by("-datetime")
            .first()
        )

        # find the latest record after the campaign
        after_record = (
            Weibo.objects(
                weibo_id=weibo_id,
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
    def get_share_growth(weibo_id, campaign_start):
        """
        Get Weibo reposts growth for a campaign
        (campaign_start -14d) → (campaign_start +14d)
        :param weibo_id:
        :param campaign_start:
        :return:
        """
        before_target = campaign_start - timedelta(days=14)
        after_target = campaign_start + timedelta(days=14)

        # find the latest record before the campaign start
        before_record = (
            Weibo.objects(
                weibo_id=weibo_id,
                datetime__lte=before_target
            )
            .order_by("-datetime")
            .first()
        )

        # find the latest record after the campaign
        after_record = (
            Weibo.objects(
                weibo_id=weibo_id,
                datetime__lte=after_target
            )
            .order_by("-datetime")
            .first()
        )
        # if not enough data, return None
        if before_record is None or after_record is None:
            return None

        before = before_record.share_count
        after = after_record.share_count

        growth_percentage = (
            round(((after - before) / before) * 100, 2)
            if before > 0 else 0
        )

        return {
            "before": {
                "date": before_record.datetime.isoformat(),
                "share_count": before_record.share_count
            },
            "after": {
                "date": after_record.datetime.isoformat(),
                "share_count": after_record.share_count
            },
            "growth": after - before,
            "percentage": growth_percentage
        }

    @staticmethod
    def get_like_growth(weibo_id, campaign_start):
        """
        Get Weibo likes growth for a campaign
        (campaign_start -14d) → (campaign_start +14d)
        :param weibo_id:
        :param campaign_start:
        :return:
        """
        before_target = campaign_start - timedelta(days=14)
        after_target = campaign_start + timedelta(days=14)

        # find the latest record before the campaign start
        before_record = (
            Weibo.objects(
                weibo_id=weibo_id,
                datetime__lte=before_target
            )
            .order_by("-datetime")
            .first()
        )

        # find the latest record after the campaign
        after_record = (
            Weibo.objects(
                weibo_id=weibo_id,
                datetime__lte=after_target
            )
            .order_by("-datetime")
            .first()
        )
        # if not enough data, return None
        if before_record is None or after_record is None:
            return None

        before = before_record.like_count
        after = after_record.like_count

        growth_percentage = (
            round(((after - before) / before) * 100, 2)
            if before > 0 else 0
        )

        return {
            "before": {
                "date": before_record.datetime.isoformat(),
                "like_count": before_record.like_count
            },
            "after": {
                "date": after_record.datetime.isoformat(),
                "like_count": after_record.like_count
            },
            "growth": after - before,
            "percentage": growth_percentage
        }

    @staticmethod
    def get_comment_growth(weibo_id, campaign_start):
        """
        Get Weibo comments growth for a campaign
        (campaign_start -14d) → (campaign_start +14d)
        :param weibo_id:
        :param campaign_start:
        :return:
        """
        before_target = campaign_start - timedelta(days=14)
        after_target = campaign_start + timedelta(days=14)

        # find the latest record before the campaign start
        before_record = (
            Weibo.objects(
                weibo_id=weibo_id,
                datetime__lte=before_target
            )
            .order_by("-datetime")
            .first()
        )

        # find the latest record after the campaign
        after_record = (
            Weibo.objects(
                weibo_id=weibo_id,
                datetime__lte=after_target
            )
            .order_by("-datetime")
            .first()
        )
        # if not enough data, return None
        if before_record is None or after_record is None:
            return None

        before = before_record.comment_count
        after = after_record.comment_count

        growth_percentage = (
            round(((after - before) / before) * 100, 2)
            if before > 0 else 0
        )

        return {
            "before": {
                "date": before_record.datetime.isoformat(),
                "comment_count": before_record.comment_count
            },
            "after": {
                "date": after_record.datetime.isoformat(),
                "comment_count": after_record.comment_count
            },
            "growth": after - before,
            "percentage": growth_percentage
        }

    @staticmethod
    def get_engage_growth(weibo_id, campaign_start):
        """
        Get Weibo engage growth for a campaign.
        Engagement count: share + comment + like
        (campaign_start -14d) → (campaign_start +14d)
        :param weibo_id:
        :param campaign_start:
        :return:
        """
        before_target = campaign_start - timedelta(days=14)
        after_target = campaign_start + timedelta(days=14)

        # find the latest record before the campaign start
        before_record = (
            Weibo.objects(
                weibo_id=weibo_id,
                datetime__lte=before_target
            )
            .order_by("-datetime")
            .first()
        )

        # find the latest record after the campaign
        after_record = (
            Weibo.objects(
                weibo_id=weibo_id,
                datetime__lte=after_target
            )
            .order_by("-datetime")
            .first()
        )
        # if not enough data, return None
        if before_record is None or after_record is None:
            return None

        before = before_record.total_eng_count
        after = after_record.total_eng_count

        growth_percentage = (
            round(((after - before) / before) * 100, 2)
            if before > 0 else 0
        )

        return {
            "before": {
                "date": before_record.datetime.isoformat(),
                "eng_count": before_record.total_eng_count
            },
            "after": {
                "date": after_record.datetime.isoformat(),
                "eng_count": after_record.total_eng_count
            },
            "growth": after - before,
            "percentage": growth_percentage
        }
