from datetime import timedelta
from models.spotify_model import Spotify


class SpotifyService:

    @staticmethod
    def get_follower_growth(spotify_id, campaign_start):
        """
        Get Spotify follower growth for a campaign
        (campaign_start -14d) → (campaign_start +14d)
        :param spotify_id:
        :param campaign_start:
        :return:
        """
        before_target = campaign_start - timedelta(days=14)
        after_target = campaign_start + timedelta(days=14)

        # find the latest record before the campaign start
        before_record = (
            Spotify.objects(
                spotify_id=spotify_id,
                datetime__lte=before_target
            )
            .order_by("-datetime")
            .first()
        )

        # find the latest record after the campaign
        after_record = (
            Spotify.objects(
                spotify_id=spotify_id,
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

        growth_percentage = round(((after-before)/before)*100, 2)

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
    def get_popularity_growth(spotify_id, campaign_start):
        """
        Get Spotify popularity growth for a campaign
        (campaign_start -14d) → (campaign_start +14d)
        :param spotify_id:
        :param campaign_start:
        :return:
        """
        before_target = campaign_start - timedelta(days=14)
        after_target = campaign_start + timedelta(days=14)

        # find the latest record before the campaign start
        before_record = (
            Spotify.objects(
                spotify_id=spotify_id,
                datetime__lte=before_target
            )
                .order_by("-datetime")
                .first()
        )

        # find the latest record after the campaign
        after_record = (
            Spotify.objects(
                spotify_id=spotify_id,
                datetime__lte=after_target
            )
                .order_by("-datetime")
                .first()
        )
        # if not enough data, return None
        if before_record is None or after_record is None:
            return None

        before = before_record.popularity
        after = after_record.popularity

        growth_percentage = round(((after - before) / before) * 100, 2)

        return {
            "before": {
                "date": before_record.datetime.isoformat(),
                "popularity": before_record.popularity
            },
            "after": {
                "date": after_record.datetime.isoformat(),
                "popularity": after_record.popularity
            },
            "growth": after - before,
            "percentage": growth_percentage
        }

    @staticmethod
    def get_monthly_listener_growth(spotify_id, campaign_start):
        """
        Get Spotify monthly listener growth for a campaign
        (campaign_start -14d) → (campaign_start +14d)
        :param spotify_id:
        :param campaign_start:
        :return:
        """
        before_target = campaign_start - timedelta(days=14)
        after_target = campaign_start + timedelta(days=14)

        # find the latest record before the campaign start
        before_record = (
            Spotify.objects(
                spotify_id=spotify_id,
                datetime__lte=before_target
            )
                .order_by("-datetime")
                .first()
        )

        # find the latest record after the campaign
        after_record = (
            Spotify.objects(
                spotify_id=spotify_id,
                datetime__lte=after_target
            )
                .order_by("-datetime")
                .first()
        )
        # if not enough data, return None
        if before_record is None or after_record is None:
            return None

        before = before_record.monthly_listener
        after = after_record.monthly_listener

        growth_percentage = round(((after - before) / before) * 100, 2)

        return {
            "before": {
                "date": before_record.datetime.isoformat(),
                "monthly_listener": before_record.monthly_listener
            },
            "after": {
                "date": after_record.datetime.isoformat(),
                "monthly_listener": after_record.monthly_listener
            },
            "growth": after - before,
            "percentage": growth_percentage
        }
