from datetime import timedelta
from models.sns.instagram_model import Instagram, InstagramLatest
from .artist_service import ArtistService
from .user_service import UserService
from rules.instagram_chart import FOLLOWER_RANGE_RULES, RANGE_DAYS, HASHTAG_RANGE_RULES
from collections import Counter, defaultdict
from .user_service import UserService


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
        is_premium = UserService.is_active_premium(user)

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
        is_premium = UserService.is_active_premium(user)

        allowed_ranges = (
            FOLLOWER_RANGE_RULES["premium"]
            if is_premium
            else FOLLOWER_RANGE_RULES["free"]
        )

        if range_key not in allowed_ranges:
            return {
                "locked": True,
                "meta": {
                    "is_premium": is_premium,
                    "range": range_key,
                    "days": None,
                    "allowed_ranges": allowed_ranges
                }
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
        is_premium = UserService.is_active_premium(user)

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
        # ---------- check if user is premium or not ----------
        is_premium = UserService.is_active_premium(user)

        allowed_ranges = (
            FOLLOWER_RANGE_RULES["premium"]
            if is_premium
            else FOLLOWER_RANGE_RULES["free"]
        )

        if range_key not in allowed_ranges:
            return {
                "locked": True,
                "meta": {
                    "is_premium": is_premium,
                    "range": range_key,
                    "days": None,
                    "allowed_ranges": allowed_ranges
                }
            }

        # ---------- calculate date ----------
        days = RANGE_DAYS[range_key]
        start_date = date_end - timedelta(days=days)

        # ----------get instagram id ----------
        instagram_id = ArtistService.get_instagram_id(artist_id)
        # print("ins id: ", instagram_id)

        pipeline = [
            # Match artist
            {"$match": {
                "user_id": instagram_id,
                "datetime": {
                    "$gt": start_date,
                    "$lte": date_end
                }
            }},
            # Sort by datetime for consistent results
            {"$sort": {"datetime": 1}},
            # Unwind posts array to work with individual posts
            {"$unwind": "$posts"},
            # Project required fields
            {"$project": {
                "_id": 0,
                "datetime": "$datetime",
                "code": "$posts.shortCode",
                "like_count": "$posts.likesCount",
            }},
            # Group by date to calculate daily totals
            {"$group": {
                "_id": "$datetime",
                "total_like": {"$sum": "$like_count"},
                "likes_per_post": {"$avg": "$like_count"},
            }},
            {"$sort": {"_id": 1}},
            {"$project": {
                "_id": 0,
                "datetime": {
                    "$dateToString": {
                        "format": "%Y-%m-%d",
                        "date": "$_id"
                    }
                },
                "total_likes": "$total_like",
                "likes_per_post": "$likes_per_post",
            }}
        ]

        records = list(InstagramLatest.objects.aggregate(*pipeline))

        # ---------- format response ----------

        return {
            "locked": False,
            "data": records,
            "meta": {
                "is_premium": is_premium,
                "range": range_key,
                "days": days,
                "allowed_ranges": allowed_ranges,
            }
        }

    @staticmethod
    def get_chart_comment(user, artist_id, date_end, range_key):
        # ---------- check if user is premium or not ----------
        is_premium = UserService.is_active_premium(user)

        allowed_ranges = (
            FOLLOWER_RANGE_RULES["premium"]
            if is_premium
            else FOLLOWER_RANGE_RULES["free"]
        )

        if range_key not in allowed_ranges:
            return {
                "locked": True,
                "meta": {
                    "is_premium": is_premium,
                    "range": range_key,
                    "days": None,
                    "allowed_ranges": allowed_ranges
                }
            }

        # ---------- calculate date ----------
        days = RANGE_DAYS[range_key]
        start_date = date_end - timedelta(days=days)

        # ----------get instagram id ----------
        instagram_id = ArtistService.get_instagram_id(artist_id)
        # print("ins id: ", instagram_id)

        pipeline = [
            # Match artist
            {"$match": {
                "user_id": instagram_id,
                "datetime": {
                    "$gt": start_date,
                    "$lte": date_end
                }
            }},
            # Sort by datetime for consistent results
            {"$sort": {"datetime": 1}},
            # Unwind posts array to work with individual posts
            {"$unwind": "$posts"},
            # Project required fields
            {"$project": {
                "_id": 0,
                "datetime": "$datetime",
                "code": "$posts.shortCode",
                "comment_count": "$posts.commentsCount",
            }},
            # Group by date to calculate daily totals
            {"$group": {
                "_id": "$datetime",
                "total_comment": {"$sum": "$comment_count"},
                "comments_per_post": {"$avg": "$comment_count"},
            }},
            {"$sort": {"_id": 1}},
            {"$project": {
                "_id": 0,
                "datetime": {
                    "$dateToString": {
                        "format": "%Y-%m-%d",
                        "date": "$_id"
                    }
                },
                "total_comments": "$total_comment",
                "comments_per_post": "$comments_per_post",
            }}
        ]

        records = list(InstagramLatest.objects.aggregate(*pipeline))

        # ---------- format response ----------

        return {
            "locked": False,
            "data": records,
            "meta": {
                "is_premium": is_premium,
                "range": range_key,
                "days": days,
                "allowed_ranges": allowed_ranges,
            }
        }

    @staticmethod
    def get_chart_engagement(user, artist_id, date_end, range_key):

        # ---------- check premium ----------
        is_premium = UserService.is_active_premium(user)

        allowed_ranges = (
            FOLLOWER_RANGE_RULES["premium"]
            if is_premium
            else FOLLOWER_RANGE_RULES["free"]
        )

        if range_key not in allowed_ranges:
            return {
                "locked": True,
                "meta": {
                    "is_premium": is_premium,
                    "range": range_key,
                    "days": None,
                    "allowed_ranges": allowed_ranges
                }
            }

        # ---------- date range ----------
        days = RANGE_DAYS[range_key]
        start_date = date_end - timedelta(days=days)

        instagram_id = ArtistService.get_instagram_id(artist_id)

        # ---------- get posts (daily snapshot) ----------
        ins_docs = (
            InstagramLatest.objects(
                user_id=instagram_id,
                datetime__gte=start_date,
                datetime__lte=date_end
            )
            .order_by("datetime")
            .only(
                "datetime",
                "posts.likesCount",
                "posts.commentsCount"
            )
        )

        # ---------- get follower snapshots ----------
        profiles = (
            Instagram.objects(
                user_id=instagram_id,
                datetime__gte=start_date,
                datetime__lte=date_end
            )
            .order_by("datetime")
            .only("follower_count", "datetime")
        )

        # ---------- build follower map ----------
        follower_map = {}
        for p in profiles:
            date_str = p.datetime.strftime("%Y-%m-%d")
            follower_map[date_str] = int(p.follower_count or 0)
        # print(follower_map)
        # ---------- no data ----------
        if not ins_docs:
            return {
                "locked": False,
                "data": [],
                "meta": {
                    "is_premium": is_premium,
                    "range": range_key,
                    "days": days,
                    "allowed_ranges": allowed_ranges,
                }
            }

        # ---------- calculate daily engagement ----------
        result = []
        last_follower = 0  # optional: fallback 用

        for doc in ins_docs:
            date_str = doc.datetime.strftime("%Y-%m-%d")

            # 取當天 follower（若沒有就用前一天）
            follower_count = follower_map.get(date_str, last_follower)
            if follower_count:
                last_follower = follower_count

            total_likes = 0
            total_comments = 0

            for post in doc.posts:
                total_likes += int(getattr(post, "like_count", 0) or 0)
                total_comments += int(getattr(post, "comment_count", 0) or 0)

            total_eng = total_likes + total_comments

            eng_rate = (
                (total_eng / follower_count) * 100
                if follower_count > 0 else 0
            )

            result.append({
                "datetime": date_str,
                "engagement_rate": round(eng_rate, 4),
            })

        return {
            "locked": False,
            "data": result,
            "meta": {
                "is_premium": is_premium,
                "range": range_key,
                "days": days,
                "allowed_ranges": allowed_ranges,
            }
        }

    @staticmethod
    def get_chart_most_used_hashtag(user, artist_id, range_key="5"):
        range_key = str(range_key)
        # ---------- check if user is premium or not ----------
        is_premium = UserService.is_active_premium(user)
        plan = "premium" if is_premium else "free"
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
        is_premium = UserService.is_active_premium(user)
        plan = "premium" if is_premium else "free"
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

    @staticmethod
    def get_latest_posts(user, artist_id):
        if not artist_id:
            raise ValueError("Missing artist_id parameter")

        # ---------- check if user is premium or not ----------
        is_premium = UserService.is_active_premium(user)
        plan = "premium" if is_premium else "free"

        # ----------get instagram id ----------
        instagram_id = ArtistService.get_instagram_id(artist_id)

        if not instagram_id:
            return {
                "locked": False,
                "data": [],
                "meta": {
                    "is_premium": is_premium,
                    "source": "instagram",
                    "reason": "no instagram id"
                }
            }

        ins_doc = (
            InstagramLatest.objects(user_id=instagram_id)
                .order_by("-datetime")
                .only("posts")
                .first()
        )

        profile = (Instagram.objects(user_id=instagram_id)
                   .only("follower_count").first()
        )

        follower_count = int(profile.follower_count or 0) \
            if profile else 0

        # ---------- no data ----------
        if not ins_doc or not ins_doc.posts:
            return {
                "locked": False,
                "data": [],
                "meta": {
                    "is_premium": is_premium,
                    "source": "instagram",
                    "reason": "no post data"
                }
            }

        # ---------- return all posts ----------
        result = []
        for post in ins_doc.posts:
            like_count = int(getattr(post, "like_count", 0) or 0)
            comment_count = int(getattr(post, "comment_count", 0) or 0)
            total_eng = like_count + comment_count
            eng_rate = (
                (total_eng / follower_count) * 100
                if follower_count > 0 else 0
            )

            result.append({
                "id": getattr(post, "id", None),
                "type": getattr(post, "type", None),
                "caption_text": getattr(post, "caption_text", None),
                "hashtags": getattr(post, "hashtag", None),
                "like_count": getattr(post, "like_count", None),
                "comment_count": getattr(post, "comment_count", None),
                "eng_rate": round(eng_rate, 4),
                "thumbnail": getattr(post, "thumbnail", None),
                "post_url": getattr(post, "post_url", None),
                "taken_at": getattr(post, "taken_at", None),
            })

        sorted_posts = sorted(
            result,
            key=lambda x: getattr(x, "taken_at", 0),
            reverse=True
        )

        return {
            "locked": False,
            "data": sorted_posts,
            "meta": {
                "is_premium": is_premium,
                "source": "instagram",
                "latest_datetime": ins_doc.datetime
            }
        }
