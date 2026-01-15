from datetime import timedelta
from models.sns.instagram_model import Instagram, InstagramLatest
from .artist_service import ArtistService
from rules.instagram_chart import FOLLOWER_RANGE_RULES, RANGE_DAYS, HASHTAG_RANGE_RULES
from collections import Counter, defaultdict


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

        growth_percentage = (
            round(((after - before) / before) * 100, 2)
            if before > 0 else 0
        )

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

        before = before_record.threads_follower or 0
        after = after_record.threads_follower or 0

        growth_percentage = (
            round(((after - before) / before) * 100, 2)
            if before > 0 else 0
        )

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

        # ----------get instagram id ----------
        instagram_id = ArtistService.get_instagram_id(artist_id)
        # print("ins id: ", instagram_id)

        records = (
            Instagram.objects(
                user_id=instagram_id,
                datetime__gt=start_date,
                datetime__lte=date_end
            )
                .order_by("datetime")
                .only("datetime", "follower_count")
        )
        # ---------- format response ----------
        data = [
            {
                "datetime": r.datetime.strftime("%Y-%m-%d"),
                "follower": r.follower_count
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
    def get_chart_threads_follower(user, artist_id, date_end, range_key):
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

        # ----------get instagram id ----------
        instagram_id = ArtistService.get_instagram_id(artist_id)
        # print("ins id: ", instagram_id)

        records = (
            Instagram.objects(
                user_id=instagram_id,
                datetime__gt=start_date,
                datetime__lte=date_end
            )
                .order_by("datetime")
                .only("datetime", "threads_follower")
        )
        # ---------- format response ----------
        data = [
            {
                "datetime": r.datetime.strftime("%Y-%m-%d"),
                "threads_follower": r.threads_follower
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
    def get_chart_post(user, artist_id, date_end, range_key):
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

        # ----------get instagram id ----------
        instagram_id = ArtistService.get_instagram_id(artist_id)
        # print("ins id: ", instagram_id)

        records = (
            Instagram.objects(
                user_id=instagram_id,
                datetime__gt=start_date,
                datetime__lte=date_end
            )
                .order_by("datetime")
                .only("datetime", "media_count")
        )
        # ---------- format response ----------
        data = [
            {
                "datetime": r.datetime.strftime("%Y-%m-%d"),
                "post_count": r.media_count
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
                "allowed_ranges": allowed_ranges,
            }
        }

    @staticmethod
    def get_chart_like(user, artist_id, date_end, range_key):
        pass

    @staticmethod
    def get_chart_comment(user, artist_id, date_end, range_key):
        pass

    @staticmethod
    def get_chart_most_used_hashtag(user, artist_id, range_key="5"):
        range_key = str(range_key)
        # ---------- check if user is premium or not ----------
        plan = "premium" if (user and user.is_premium) else "free"
        rule = HASHTAG_RANGE_RULES[plan]

        # ---------- validate range ----------
        if range_key not in rule["ranges"]:
            raise PermissionError(
                f"Range {range_key} not allowed for plan {plan}"
            )

        video_limit = int(range_key)
        hashtag_limit = rule["hashtag_limit"]

        # ----------get instagram id ----------
        instagram_id = ArtistService.get_instagram_id(artist_id)

        ins_doc = (
            InstagramLatest.objects(user_id=instagram_id)
                .order_by("-datetime")
                .only("posts")
                .first()
        )

        if not ins_doc or not ins_doc.posts:
            return {
                "locked": False,
                "data": [],
                "meta": {
                    "is_premium": user.is_premium if user else False,
                    "video_limit": video_limit,
                    "hashtag_limit": hashtag_limit
                }
            }

        # get latest N posts
        latest_posts  = ins_doc.posts[:video_limit]

        hashtags = []

        for post in latest_posts:
            if post.hashtag:
                hashtags.extend(post.hashtag)

        # ---------- count hashtags ----------
        counter = Counter(hashtags)

        result = [
            {"_id": tag, "count": count}
                for tag, count in counter.most_common(hashtag_limit)
        ]

        return {
            "locked": False,
            "data": result,
            "meta": {
                "is_premium": user.is_premium if user else False,
                "video_limit": video_limit,
                "hashtag_limit": hashtag_limit
            }
        }

    @staticmethod
    def get_chart_most_engaged_hashtag(user, artist_id, range_key="5"):
        range_key = str(range_key)
        # ---------- check if user is premium or not ----------
        plan = "premium" if (user and user.is_premium) else "free"
        rule = HASHTAG_RANGE_RULES[plan]

        # ---------- validate range ----------
        if range_key not in rule["ranges"]:
            raise PermissionError(
                f"Range {range_key} not allowed for plan {plan}"
            )

        video_limit = int(range_key)
        hashtag_limit = rule["hashtag_limit"]

        # ----------get instagram id ----------
        instagram_id = ArtistService.get_instagram_id(artist_id)

        # ---------- get instagram latest follower ---------
        ins_latest_follower = (
            Instagram.objects(user_id=instagram_id)
                .order_by("-datetime")
                .only("follower_count")
                .first()
        )
        # if follower is None
        follower = int(ins_latest_follower.follower_count or 0)
        if follower <= 0:
            follower = 1

        ins_doc = (
            InstagramLatest.objects(user_id=instagram_id)
                .order_by("-datetime")
                .only("posts")
                .first()
        )

        if not ins_doc or not ins_doc.posts:
            return {
                "locked": False,
                "data": [],
                "meta": {
                    "is_premium": user.is_premium if user else False,
                    "video_limit": video_limit,
                    "hashtag_limit": hashtag_limit
                }
            }

        # ---------- calculate engagement per hashtag ----------
        hashtag_counter = defaultdict(int)
        hashtag_eng_sum = defaultdict(float)

        latest_posts = ins_doc.posts[:video_limit]

        for post in latest_posts:
            if not post.hashtag:
                continue

            like = int(post.like_count or 0)
            comment = int(post.comment_count or 0)
            sub_total = like + comment

            eng_rate = sub_total / follower

            for tag in post.hashtag:
                hashtag_counter[tag] += 1
                hashtag_eng_sum[tag] += eng_rate

        # ---------- average eng rate per hashtag ----------
        result = []
        for tag, count in hashtag_counter.items():
            avg_eng_rate = (hashtag_eng_sum[tag] / count) * 100
            result.append({
                "_id": tag,
                "eng_rate": round(avg_eng_rate, 4)
            })

        # ---------- sort & limit ----------
        result.sort(
            key=lambda x: x["eng_rate"],
            reverse=True
        )

        return {
            "locked": False,
            "data": result[:hashtag_limit],
            "meta": {
                "post_count": len(ins_doc.posts),
                "follower": follower
            }
        }
