from datetime import timedelta
from models.sns.youtube_model import Youtube
from rules.youtube_chart import FOLLOWER_RANGE_RULES, RANGE_DAYS, HASHTAG_RANGE_RULES
from .artist_service import ArtistService
from .user_service import UserService
import pandas as pd
import numpy as np


def to_int(value, default=0):
    try:
        return int(value)
    except (TypeError, ValueError):
        return default

def extract_hashtags_keyword(text):
    """
    extract keywords with hashtag from string
    """
    hashtag_list = []

    # splitting the text into words
    for word in text.split():
        # checking the first character of every word
        if word[0] == '#':
            # adding the word to the hashtag_list
            hashtag_list.append(word[1:])
    return hashtag_list

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

        growth_percentage = (
            round(((after - before) / before) * 100, 2)
            if before > 0 else 0
        )

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

        growth_percentage = (
            round(((after - before) / before) * 100, 2)
            if before > 0 else 0
        )

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

        growth_percentage = (
            round(((after - before) / before) * 100, 2)
            if before > 0 else 0
        )

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

        # ----------get youtube id ----------
        youtube_id = ArtistService.get_youtube_id(artist_id)
        # print("yt id: ", youtube_id)

        records = (
            Youtube.objects(
                channel_id=youtube_id,
                datetime__gt=start_date,
                datetime__lte=date_end
            )
                .order_by("datetime")
                .only("datetime", "subscriber_count", "view_count", "video_count", "channel_hashtag", "video_hashtag")
        )
        # ---------- format response ----------
        data = [
            {
                "datetime": r.datetime.strftime("%Y-%m-%d"),
                "follower": to_int(r.subscriber_count),
                "video_count": to_int(r.video_count),
                "view_count": to_int(r.view_count),
                "video_hashtag": to_int(r.video_hashtag),
                "channel_hashtag": to_int(r.channel_hashtag)
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
    def get_chart_video_view(user, artist_id, date_end, range_key):
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
        days = RANGE_DAYS[range_key]
        start_date = date_end - timedelta(days=days)

        # ----------get youtube id ----------
        youtube_id = ArtistService.get_youtube_id(artist_id)
        # print("yt id: ", youtube_id)

        # pipeline
        pipeline = [
            {"$match": {
                "channel_id": youtube_id
            }},
            {"$sort": {"datetime": -1}},
            {"$match": {
                "datetime": {
                    "$lte": date_end,
                    "$gt": start_date
                }
            }},
            {"$unwind": "$video"},
            {"$project": {
                "_id": 0,
                "datetime": "$datetime",
                "video_publish_at": "$video.published_at",
                "video_view": "$video.view_count"
            }},
            {"$group": {
                "_id": "$datetime",
                "latest_ten": {"$push": "$$ROOT"}
            }},
            {"$project": {
                "_id": 1,
                "videos": {
                    "$slice": [{
                        "$map": {
                            "input": "$latest_ten",
                            "as": "video",
                            "in": {
                                "datetime": "$$video.datetime",
                                "video_publish_at": {
                                    "$dateFromString": {
                                        "dateString": "$$video.video_publish_at",
                                        "format": "%Y-%m-%dT%H:%M:%SZ"
                                    }
                                },
                                "video_view": {
                                    "$convert": {
                                        "input": "$$video.video_view",
                                        "to": "long",
                                        "onError": 0,
                                        "onNull": 0
                                    }
                                }
                            }
                        }
                    }, 12]
                }
            }},
            {"$addFields": {
                "total_view": {
                    # Sum all video_view values in the array
                    "$sum": "$videos.video_view"
                }
            }},
            {"$sort": {"_id": 1}},
            {"$project": {
                "_id": 0,
                "datetime": {"$dateToString": {
                    "format": "%Y-%m-%d",
                    "date": "$_id"
                }},
                "total_video_view": "$total_view"
            }}
        ]

        # Execute pipeline
        results = Youtube.objects().aggregate(pipeline)

        # Format results
        result = list(results)

        # ---------- format response ----------

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
    def get_chart_video_likes_and_comments(user, artist_id, date_end, range_key):
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
        days = RANGE_DAYS[range_key]
        start_date = date_end - timedelta(days=days)

        # ----------get youtube id ----------
        youtube_id = ArtistService.get_youtube_id(artist_id)
        # print("yt id: ", youtube_id)

        # pipeline
        pipeline = [
            {"$match": {
                "channel_id": youtube_id
            }},
            {"$sort": {"datetime": -1}},
            {"$limit": days},
            # match date range
            {"$match": {
                "datetime": {
                    "$lte": date_end,
                    "$gt": start_date
                }
            }},
            # unwind video
            {"$unwind": "$video"},
            {"$project": {
                "_id": 0,
                "datetime": {
                    "$dateToString": {
                        "format": "%Y-%m-%d",
                        "date": "$datetime"
                    }
                },
                "published_at": "$video.published_at",
                "view_count": {"$toLong": "$video.view_count"},
                "like_count": {"$toInt": "$video.like_count"},
                "favorite_count": {"$toInt": "$video.favorite_count"},
                "comment_count": {"$toInt": "$video.comment_count"}
            }},
            # group videos by date
            {"$group": {
                "_id": "$datetime",
                "video": {"$sum": {"$toInt": 1}},
                "total_view": {"$sum": "$view_count"},
                "total_like": {"$sum": "$like_count"},
                "total_favorite": {"$sum": "$favorite_count"},
                "total_comment": {"$sum": "$comment_count"}
            }},
            {"$sort": {"_id": 1}},
            # # calculate subtotal
            {"$addFields": {
                "sub_total": {
                    "$sum": ["$total_like", "$total_favorite", "$total_comment"]
                }
            }},
            # calculate engagement rate & avg
            {"$project": {
                "_id": 0,
                "datetime": "$_id",
                "video": "$video",
                "total_view": "$total_view",
                "total_like": "$total_like",
                "avg_like": {
                    "$divide": ["$total_like", "$video"]
                },
                "total_comment": "$total_comment",
                "avg_comment": {
                    "$divide": ["$total_comment", "$video"]
                },
                # "eng_rate": {
                #         "$multiply": [{
                #             "$divide": ["$sub_total", "$total_view"]
                #         }, 100]
                # }
            }}
        ]

        # Execute pipeline
        results = Youtube.objects().aggregate(pipeline)

        # Format results
        result = list(results)

        # ---------- format response ----------
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
    def get_chart_most_used_hashtag(user, artist_id, range_key="5"):
        range_key = str(range_key)
        # ---------- check if user is premium or not ----------
        is_premium = UserService.is_active_premium(user)
        plan = "premium" if is_premium else "free"
        rule = HASHTAG_RANGE_RULES[plan]

        # ---------- validate range ----------
        if range_key not in rule["ranges"]:
            return {
                "locked": True,
                "data": [],
                "meta": {
                    "is_premium": is_premium,
                    "allowed_ranges": rule["ranges"],
                    "hashtag_limit": rule["hashtag_limit"]
                }
            }

        video_limit = int(range_key)
        hashtag_limit = rule["hashtag_limit"]

        # ----------get youtube id ----------
        youtube_id = ArtistService.get_youtube_id(artist_id)

        youtube_doc = (
            Youtube.objects(channel_id=youtube_id)
                .order_by("-datetime")
                .only("video")
                .first()
        )

        if not youtube_doc or not youtube_doc.video:
            return {
                "locked": False,
                "data": [],
                "meta": {
                    "is_premium": is_premium,
                    "allowed_ranges": rule["ranges"],
                    "hashtag_limit": hashtag_limit
                }
            }

        # get latest N videos
        videos = youtube_doc.video[:video_limit]

        titles_hashtags = []
        tags_hashtags = []

        for video in videos:
            # title hashtags
            title = video.title or ""
            title = title.replace("#", " #")
            titles_hashtags.extend(
                extract_hashtags_keyword(title)
            )

            # tags hashtags
            if video.tags:
                tags_hashtags.extend(video.tags)

        # calculate counts
        joined_list = titles_hashtags + tags_hashtags
        if not joined_list:
            return {
                "locked": False,
                "data": [],
                "meta": {
                    "is_premium": is_premium,
                    "allowed_ranges": rule["ranges"],
                    "hashtag_limit": hashtag_limit
                }
            }

        w = pd.value_counts(np.array(joined_list))

        df = pd.DataFrame(
            list(zip(w.keys(), w)),
            columns=["_id", "count"]
        )

        return {
            "locked": False,
            "data": df.to_dict(orient="records")[:hashtag_limit],
            "meta": {
                "is_premium": is_premium,
                "allowed_ranges": rule["ranges"],
                "hashtag_limit": hashtag_limit
            }
        }

    @staticmethod
    def get_chart_most_engaged_hashtag(user, artist_id, range_key="5"):
        range_key = str(range_key)
        # check if user is premium or not
        is_premium = UserService.is_active_premium(user)
        plan = "premium" if is_premium else "free"
        rule = HASHTAG_RANGE_RULES[plan]

        #validate range
        if range_key not in rule["ranges"]:
            return {
                "locked": True,
                "data": [],
                "meta": {
                    "is_premium": is_premium,
                    "allowed_ranges": rule["ranges"],
                    "hashtag_limit": rule["hashtag_limit"]
                }
            }

        video_limit = int(range_key)
        hashtag_limit = rule["hashtag_limit"]

        # get youtube id
        youtube_id = ArtistService.get_youtube_id(artist_id)

        youtube_doc = (
            Youtube.objects(channel_id=youtube_id)
                .order_by("-datetime")
                .only("video")
                .first()
        )

        if not youtube_doc or not youtube_doc.video:
            return {
                "locked": False,
                "data": [],
                "meta": {
                    "is_premium": is_premium,
                    "allowed_ranges": rule["ranges"],
                    "hashtag_limit": rule["hashtag_limit"]
                }
            }

        videos = youtube_doc.video[:video_limit]

        hashtag_eng_map = {}  # { hashtag: [eng_rate, eng_rate, ...] }

        for video in videos:
            view_count = int(video.view_count or 0)
            if view_count == 0:
                continue

            sub_total = (video.like_count or 0) + (video.comment_count or 0)
            eng_rate = sub_total / view_count  # raw rate (0.x)

            hashtags = []

            # title hashtags
            title = (video.title or "").replace("#", " #")
            hashtags.extend(extract_hashtags_keyword(title))

            # tag hashtags
            if video.tags:
                hashtags.extend(video.tags)

            for tag in hashtags:
                if not tag:
                    continue
                hashtag_eng_map.setdefault(tag, []).append(eng_rate)

        if not hashtag_eng_map:
            return {
                "locked": False,
                "data": [],
                "meta": {
                    "is_premium": is_premium,
                    "allowed_ranges": rule["ranges"],
                    "hashtag_limit": hashtag_limit
                }
            }

        # calculate avg engagement rate
        result = []
        for tag, rates in hashtag_eng_map.items():
            avg_rate = sum(rates) / len(rates) * 100  # %
            result.append({
                "_id": tag,
                "eng_rate": round(avg_rate, 4)
            })

        # sort & limit
        result.sort(key=lambda x: x["eng_rate"], reverse=True)

        return {
            "locked": False,
            "data": result[:hashtag_limit],
            "meta": {
                "is_premium": is_premium,
                "allowed_ranges": rule["ranges"],
                "hashtag_limit": hashtag_limit
            }
        }

    @staticmethod
    def get_posts(artist_id):
        if not artist_id:
            raise ValueError("Missing artist_id parameter")

        # ---------- get youtube id ----------
        youtube_id = ArtistService.get_youtube_id(artist_id)

        youtube_doc = (
            Youtube.objects(channel_id=youtube_id)
                .order_by("-datetime")
                .only("datetime", "channel_id", "video")
                .first()
        )

        if not youtube_doc or not youtube_doc.video:
            return []

        result = []

        for video in youtube_doc.video:
            view_count = int(video.view_count or 0)
            like_count = int(video.like_count or 0)
            comment_count = int(video.comment_count or 0)

            eng_rate = (
                ((like_count + comment_count) / view_count) * 100
                if view_count > 0 else 0
            )

            result.append({
                "datetime": youtube_doc.datetime,
                "channel_id": youtube_doc.channel_id,
                "published_at": video.published_at,
                "title": video.title,
                "thumbnail": video.thumbnail,
                "tags": video.tags,
                "url": f"https://www.youtube.com/watch?v={video.code}",
                "category_id": video.category_id,
                "view_count": view_count,
                "comment_count": comment_count,
                "like_count": like_count,
                "favorite_count": int(video.favorite_count or 0),
                "eng_rate": round(eng_rate, 4)
            })

        return result
