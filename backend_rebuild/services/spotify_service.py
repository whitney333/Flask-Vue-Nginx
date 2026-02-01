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

        growth_percentage = (
            round(((after - before) / before) * 100, 2)
            if before > 0 else 0
        )

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

        growth_percentage = (
            round(((after - before) / before) * 100, 2)
            if before > 0 else 0
        )

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

    @staticmethod
    def get_top_five_city_growth(spotify_id, campaign_start):
        """
            Get Spotify top five city growth for a campaign
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

        before_top = before_record.top_country or []
        after_top = after_record.top_country or []

        # convert list of object to dict
        def normalize(top_country):
            result = {}
            for c in top_country:
                result[c["city"]] = {
                    "city": c["city"],
                    "country": c["country"],
                    "listener": int(c["listener"])
                }
            return result

        before_map = normalize(before_top)
        after_map = normalize(after_top)

        # merge before & after
        cities = []
        all_cities = set(before_map.keys()) | set(after_map.keys())

        for city in all_cities:
            before = before_map.get(city, {}).get("listener", 0)
            after = after_map.get(city, {}).get("listener", 0)

            growth_pct = None
            if before > 0:
                growth_pct = round((after - before) / before * 100, 1)

            cities.append({
                "city": city,
                "country": (
                        after_map.get(city, {}).get("country")
                        or before_map.get(city, {}).get("country")
                ),
                "before": before,
                "after": after,
                "growth_pct": growth_pct
            })

        # 5️⃣ 依 after listener 排序，取 Top 5（After 視角）
        cities.sort(key=lambda x: x["after"], reverse=True)
        top_five = cities[:5]

        # 6️⃣ Mini KPI
        top_city = top_five[0] if top_five else None

        fastest_growing = max(
            [c for c in top_five if c["growth_pct"] is not None],
            key=lambda x: x["growth_pct"],
            default=None
        )

        new_market = next(
            (c for c in top_five if c["before"] == 0 and c["after"] > 0),
            None
        )

        # 7️⃣ 回傳
        return {
            "kpi": {
                "top_city": top_city,
                "fastest_growing_city": fastest_growing,
                "new_market": new_market
            },
            "chart": {
                "cities": top_five
            },
            "meta": {
                "before_snapshot": before_record["datetime"],
                "after_snapshot": after_record["datetime"],
                "comparison": "snapshot vs snapshot",
                "unit": "listeners"
            }
        }
