from datetime import timedelta
from models.sns.instagram_model import Instagram


class InstagramService:

    @staticmethod
    def get_follower_growth(instagram_id, campaign_start):
        """
            Get Instagram follower growth for a campaign
            (campaign_start -14d) → (campaign_start +14d)
            :param instagram_id:
            :param campaign_start:
            :return:
        """
        before_target = campaign_start - timedelta(days=14)
        after_target = campaign_start + timedelta(days=14)

        # find the latest record before the campaign start
        before_record = (
            Instagram.objects(
                user_id=instagram_id,
                datetime__lte=before_target
            )
                .order_by("-datetime")
                .first()
        )

        # find the latest record after the campaign
        after_record = (
            Instagram.objects(
                user_id=instagram_id,
                datetime__lte=after_target
            )
                .order_by("-datetime")
                .first()
        )
        # if not enough data, return None
        if before_record is None or after_record is None:
            return None

        before = before_record.follower_count
        after = after_record.follower_count

        growth_percentage = round(((after - before) / before) * 100, 2)

        return {
            "before": {
                "date": before_record.datetime.isoformat(),
                "follower": before_record.follower_count
            },
            "after": {
                "date": after_record.datetime.isoformat(),
                "follower": after_record.follower_count
            },
            "growth": after - before,
            "percentage": growth_percentage
        }

    @staticmethod
    def get_threads_follower_growth(instagram_id, campaign_start):
        """
            Get Instagram Threads follower growth for a campaign
            (campaign_start -14d) → (campaign_start +14d)
            :param instagram_id:
            :param campaign_start:
            :return:
        """
        before_target = campaign_start - timedelta(days=14)
        after_target = campaign_start + timedelta(days=14)

        # find the latest record before the campaign start
        before_record = (
            Instagram.objects(
                user_id=instagram_id,
                datetime__lte=before_target
            )
                .order_by("-datetime")
                .first()
        )

        # find the latest record after the campaign
        after_record = (
            Instagram.objects(
                user_id=instagram_id,
                datetime__lte=after_target
            )
                .order_by("-datetime")
                .first()
        )
        # if not enough data, return None
        if before_record is None or after_record is None:
            return None

        before = before_record.threads_follower
        after = after_record.threads_follower

        growth_percentage = round(((after - before) / before) * 100, 2)

        return {
            "before": {
                "date": before_record.datetime.isoformat(),
                "threads_follower": before_record.threads_follower
            },
            "after": {
                "date": after_record.datetime.isoformat(),
                "threads_follower": after_record.threads_follower
            },
            "growth": after - before,
            "percentage": growth_percentage
        }

    @staticmethod
    def get_engagement_growth(instagram_id, campaign_start):
        pass
