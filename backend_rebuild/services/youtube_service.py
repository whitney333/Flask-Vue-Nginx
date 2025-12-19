from datetime import timedelta
from models.sns.youtube_model import Youtube


def to_int(value, default=0):
    try:
        return int(value)
    except (TypeError, ValueError):
        return default

class YoutubeService:

    @staticmethod
    def get_follower_growth(youtube_id, campaign_start):
        """
            Get YouTube follower growth for a campaign
            (campaign_start -14d) → (campaign_start +14d)
            :param youtube_id:
            :param campaign_start:
            :return:
        """
        before_target = campaign_start - timedelta(days=14)
        after_target = campaign_start + timedelta(days=14)

        # find the latest record before the campaign start
        before_record = (
            Youtube.objects(
                channel_id=youtube_id,
                datetime__lte=before_target
            )
            .order_by("-datetime")
            .first()
        )

        # find the latest record after the campaign
        after_record = (
            Youtube.objects(
                channel_id=youtube_id,
                datetime__lte=after_target
            )
            .order_by("-datetime")
            .first()
        )
        # if not enough data, return None
        if before_record is None or after_record is None:
            return None

        before = before_record.subscriber_count
        after = after_record.subscriber_count

        growth_percentage = round(((after - before) / before) * 100, 2)

        return {
            "before": {
                "date": before_record.datetime.isoformat(),
                "follower": before_record.subscriber_count
            },
            "after": {
                "date": after_record.datetime.isoformat(),
                "follower": after_record.subscriber_count
            },
            "growth": after - before,
            "percentage": growth_percentage
        }

    @staticmethod
    def get_channel_hashtag_growth(youtube_id, campaign_start):
        """
            Get YouTube channel hashtag growth for a campaign
            (campaign_start -14d) → (campaign_start +14d)
            :param youtube_id:
            :param campaign_start:
            :return:
        """
        before_target = campaign_start - timedelta(days=14)
        after_target = campaign_start + timedelta(days=14)

        # find the latest record before the campaign start
        before_record = (
            Youtube.objects(
                channel_id=youtube_id,
                datetime__lte=before_target
            )
            .order_by("-datetime")
            .first()
        )

        # find the latest record after the campaign
        after_record = (
            Youtube.objects(
                channel_id=youtube_id,
                datetime__lte=after_target
            )
            .order_by("-datetime")
            .first()
        )
        # if not enough data, return None
        if before_record is None or after_record is None:
            return None

        before = before_record.channel_hashtag
        after = after_record.channel_hashtag

        growth_percentage = round(((after - before) / before) * 100, 2)

        return {
            "before": {
                "date": before_record.datetime.isoformat(),
                "channel_hashtag": before_record.channel_hashtag
            },
            "after": {
                "date": after_record.datetime.isoformat(),
                "channel_hashtag": after_record.channel_hashtag
            },
            "growth": after - before,
            "percentage": growth_percentage
        }

    @staticmethod
    def get_video_hashtag_growth(youtube_id, campaign_start):
        """
            Get YouTube video hashtag growth for a campaign
            (campaign_start -14d) → (campaign_start +14d)
            :param youtube_id:
            :param campaign_start:
            :return:
        """
        before_target = campaign_start - timedelta(days=14)
        after_target = campaign_start + timedelta(days=14)

        # find the latest record before the campaign start
        before_record = (
            Youtube.objects(
                channel_id=youtube_id,
                datetime__lte=before_target
            )
            .order_by("-datetime")
            .first()
        )

        # find the latest record after the campaign
        after_record = (
            Youtube.objects(
                channel_id=youtube_id,
                datetime__lte=after_target
            )
            .order_by("-datetime")
            .first()
        )
        # if not enough data, return None
        if before_record is None or after_record is None:
            return None

        before = before_record.video_hashtag
        after = after_record.video_hashtag

        growth_percentage = round(((after - before) / before) * 100, 2)

        return {
            "before": {
                "date": before_record.datetime.isoformat(),
                "channel_hashtag": before_record.video_hashtag
            },
            "after": {
                "date": after_record.datetime.isoformat(),
                "channel_hashtag": after_record.video_hashtag
            },
            "growth": after - before,
            "percentage": growth_percentage
        }

    @staticmethod
    def get_engagement_growth(youtube_id, campaign_start):
        """
        Get YouTube video hashtag growth for a campaign
        (campaign_start -14d) → (campaign_start +14d)
        :param youtube_id:
        :param campaign_start:
        :return:
        """
        before_target = campaign_start - timedelta(days=14)
        after_target = campaign_start + timedelta(days=14)

        # find the latest record before the campaign start
        before_record = (
            Youtube.objects(
                channel_id=youtube_id,
                datetime__lte=before_target
            )
            .order_by("-datetime")
            .first()
        )

        # find the latest record after the campaign
        after_record = (
            Youtube.objects(
                channel_id=youtube_id,
                datetime__lte=after_target
            )
            .order_by("-datetime")
            .first()
        )

        # if not enough data, return None
        if before_record is None or after_record is None:
            return None

        before = before_record.video
        after = after_record.video

        # calculate engagement
        before_engagement_list = []
        after_engagement_list = []

        for item in before:
            like = to_int(item.like_count)
            comment = to_int(item.comment_count)
            view = to_int(item.view_count)

            if view > 0:
                score = like + comment
                before_engagement_list.append(score / view)

        for item in after:
            like = to_int(item.like_count)
            comment = to_int(item.comment_count)
            view = to_int(item.view_count)

            if view > 0:
                score = like + comment
                after_engagement_list.append(score / view)

        # engagement growth
        before_rate = sum(before_engagement_list) / len(before_engagement_list)
        after_rate = sum(after_engagement_list) / len(after_engagement_list)

        growth_percentage = round(
            ((after_rate - before_rate) / before_rate) * 100, 2
        ) if before_rate > 0 else None

        return {
            "before": {
                "date": before_record.datetime.isoformat(),
                "engagement": before_rate
            },
            "after": {
                "date": after_record.datetime.isoformat(),
                "engagement": after_rate
            },
            "percentage": growth_percentage
        }

