from datetime import timedelta
from models.spotify_model import Spotify, SpotifyCharts, SpotifyOst
from rules.music_chart import FOLLOWER_RANGE_RULES, RANGE_DAYS
from .artist_service import ArtistService
from .user_service import UserService
import logging

logger = logging.getLogger(__name__)


class SpotifyService:
    ##### for chart #####
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

    @staticmethod
    def get_chart_follower(user, artist_id, date_end, range_key):
        # ---------- check if user is premium or not ----------
        is_premium = UserService.is_active_premium(user)

        allowed_ranges = (
            FOLLOWER_RANGE_RULES["premium"]
            if is_premium
            else FOLLOWER_RANGE_RULES["free"]
        )
        logger.debug(f"is_premium: {is_premium}, range_key: {range_key}, allowed: {allowed_ranges}")
        if range_key not in allowed_ranges:
            return {
                "locked": True,
                "meta": {
                    "is_premium": is_premium,
                    "allowed_ranges": allowed_ranges
                }
            }

        # ---------- calculate date ----------
        days = RANGE_DAYS[range_key]
        start_date = date_end - timedelta(days=days)

        # ----------get spotify id ----------
        spotify_id = ArtistService.get_spotify_id(artist_id)
        # print("sp id: ", spotify_id)

        records = (
            Spotify.objects(
                spotify_id=spotify_id,
                datetime__gt=start_date,
                datetime__lte=date_end
            )
                .order_by("datetime")
                .only("datetime", "follower")
        )
        # ---------- format response ----------
        data = [
            {
                "datetime": r.datetime.strftime("%Y-%m-%d"),
                "follower": r.follower
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
    def get_chart_monthly_listener(user, artist_id, date_end, range_key):
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
                    "allowed_ranges": allowed_ranges
                }
            }

        # ---------- calculate date ----------
        days = RANGE_DAYS[range_key]
        start_date = date_end - timedelta(days=days)

        # ----------get spotify id ----------
        spotify_id = ArtistService.get_spotify_id(artist_id)
        # print("sp id: ", spotify_id)

        records = (
            Spotify.objects(
                spotify_id=spotify_id,
                datetime__gt=start_date,
                datetime__lte=date_end
            )
                .order_by("datetime")
                .only("datetime", "monthly_listener")
        )
        # ---------- format response ----------
        data = [
            {
                "datetime": r.datetime.strftime("%Y-%m-%d"),
                "monthly_listener": r.monthly_listener
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
    def get_chart_popularity(user, artist_id, date_end, range_key):
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
                    "allowed_ranges": allowed_ranges
                }
            }

        # ---------- calculate date ----------
        days = RANGE_DAYS[range_key]
        start_date = date_end - timedelta(days=days)

        # ----------get spotify id ----------
        spotify_id = ArtistService.get_spotify_id(artist_id)
        # print("sp id: ", spotify_id)

        records = (
            Spotify.objects(
                spotify_id=spotify_id,
                datetime__gt=start_date,
                datetime__lte=date_end
            )
                .order_by("datetime")
                .only("datetime", "popularity")
        )
        # ---------- format response ----------
        data = [
            {
                "datetime": r.datetime.strftime("%Y-%m-%d"),
                "popularity": r.popularity
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
    def get_chart_fan_conversion_rate(user, artist_id, date_end, range_key):
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
                    "allowed_ranges": allowed_ranges
                }
            }

        # ---------- calculate date ----------
        days = RANGE_DAYS[range_key]
        start_date = date_end - timedelta(days=days)

        # ----------get spotify id ----------
        spotify_id = ArtistService.get_spotify_id(artist_id)
        # print("sp id: ", spotify_id)

        pipeline = [
            # match artist spotify id
            {"$match": {
                "spotify_id": str(spotify_id)
            }},
            # sort by datetime
            {"$sort": {"datetime": 1}},
            # match date range
            {"$match": {
                "datetime": {
                    "$lte": date_end,
                    "$gt": start_date
                }
            }},
            {"$project": {
                "_id": 0,
                "id": "$spotify_id",
                "date": {
                    "$dateToString": {
                        "format": "%Y-%m-%d",
                        "date": "$datetime"
                    }
                },
                "follower": "$follower",
                "monthly_listener": "$monthly_listener"
            }},
            # add conversion rate field
            {"$project": {
                "_id": 0,
                "datetime": "$date",
                "conversion_rate": {
                    "$multiply": [{"$divide": ["$follower", "$monthly_listener"]}, 100]
                }
            }}
        ]

        # Execute pipeline
        results = Spotify.objects().aggregate(pipeline)

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
    def get_chart_top_city(user, artist_id):
        # ---------- check if user is premium or not ----------
        is_premium = UserService.is_active_premium(user)

        # ----------get spotify id ----------
        spotify_id = ArtistService.get_spotify_id(artist_id)
        # print("sp id: ", spotify_id)

        record = (
            Spotify.objects(spotify_id=spotify_id)
                .order_by("-datetime")
                .only("datetime", "spotify_id", "top_country")
                .first()
        )

        if not record or not record.top_country:
            return {
                "data": [],
                "meta": {
                    "is_premium": is_premium
                }
            }

        # ---------- format response ----------
        result = [
            {
                "datetime": record.datetime.strftime("%Y-%m-%d"),
                "id": record.spotify_id,
                "top_city": [
                    {
                        "city": city.city,
                        "country": city.country,
                        "listener": int(city.listener)
                    }
                    for city in record.top_country
                ]
            }
        ]

        return {
            "data": result,
            "meta": {
                "is_premium": is_premium
            }
        }

    @staticmethod
    def get_chart_top_track_by_region(user, artist_id, country):
        # ---------- check if user is premium or not ----------
        is_premium = UserService.is_active_premium(user)

        # ----------get spotify id ----------
        spotify_id = ArtistService.get_spotify_id(artist_id)
        # print("sp id: ", spotify_id)

        if not spotify_id:
            return {
                "locked": False,
                "data": [],
                "tracks": [],
                "meta": {
                    "is_premium": is_premium
                }
            }

        # ---------- pipelines ----------
        get_track_title_pipeline = [
            {"$match": {
                "spotify_id": spotify_id
            }},
            {"$sort": {"datetime": -1}},
            {"$limit": 1},
            {"$unwind": "$top_track"},
            {"$project": {
                "tracks": "$top_track.tracks"
            }},
            {"$unwind": "$tracks"},
            {"$group": {
                "_id": None,
                "tracks": {
                    "$addToSet": "$tracks.track"
                }
            }},
            {"$project": {"_id": 0}}
        ]

        pipeline = [
            {"$match": {
                "spotify_id": spotify_id
            }},
            {"$sort": {"datetime": -1}},
            {"$limit": 1},
            {"$unwind": "$top_track"},
            {"$project": {
                "region": "$top_track.region",
                "tracks": "$top_track.tracks"
            }},
            {"$unwind": "$tracks"},
            {"$group": {
                "_id": {
                    "region": "$region",
                    "track": "$tracks.track"
                },
                "popularity": {
                    "$avg": "$tracks.popularity"
                }
            }},
            {"$group": {
                "_id": "$_id.track",
                "track_info": {
                    "$push": {
                        "region": "$_id.region",
                        "agg_popularity": {
                            "$round": ["$popularity", 2]}
                    }
                }
            }},
            {"$project": {
                "_id": 0,
                "track_info": 1
            }}
        ]

        track_list = Spotify.objects.aggregate(*get_track_title_pipeline)
        track_list_result = list(track_list)

        _result = Spotify.objects.aggregate(*pipeline)
        result = list(_result)

        if not is_premium:
            # free user: get the first data
            result = result[:1]
        else:
            # premium user: get the first ten
            result = result[:10]

        return {
            "locked": False,
            "data": result,
            "tracks": track_list_result,
            "meta": {
                "is_premium": True
            }
        }

    @staticmethod
    def get_chart_top_track_by_country(user, artist_id, country):
        # ---------- check if user is premium or not ----------
        is_premium = UserService.is_active_premium(user)

        # ----------get spotify id ----------
        spotify_id = ArtistService.get_spotify_id(artist_id)
        # print("sp id: ", spotify_id)

        pipeline = [
            {"$match": {
                "spotify_id": spotify_id
            }},
            {"$sort": {"datetime": -1}},
            {"$limit": 1},
            {"$unwind": "$top_track"},
            # match country
            {"$match": {
                "top_track.country": country
            }},
            {"$project": {
                "_id": 0,
                "datetime": {
                    "$dateToString": {
                        "format": "%Y-%m-%d",
                        "date": "$datetime"
                    }
                },
                "country": "$top_track.country",
                "top_track": "$top_track.tracks",
            }},
            {"$unwind": "$top_track"},
            {"$sort": {"top_track.popularity": -1}},
            {"$group": {
                "_id": {
                    "datetime": "$datetime",
                    "country": "$country"
                },
                "top_track": {"$push": "$top_track"}
            }},
            {"$project": {
                "_id": 0,
                "datetime": "$_id.datetime",
                "country": "$_id.country",
                "top_track": "$top_track"
            }}
        ]

        results = Spotify.objects.aggregate(*pipeline)
        result = list(results)

        if not result:
            return {
                "locked": False,
                "data": [],
                "meta": {
                    "is_premium": is_premium
                }
            }

        # ---------- format response ----------
        return {
            "locked": False,
            "data": result,
            "meta": {
                "is_premium": is_premium,
            }
        }

    ##### for trending artists #####
    @classmethod
    def get_trending_artist_popularity(cls, spotify_ids):
        """
            Return:
            {
                "spotify_id_1": popularity,
                "spotify_id_2": popularity,
                ...
            }
        """
        if not spotify_ids:
            return {}

        docs = (
            Spotify.objects(spotify_id__in=spotify_ids)
                .order_by("-datetime")
                .only("spotify_id", "popularity")
        )

        popularity_map = {}
        for doc in docs:
            if doc.spotify_id not in popularity_map:
                popularity_map[doc.spotify_id] = doc.popularity

        return popularity_map

    @staticmethod
    def get_trending_artist_chart_score(country, year, week):
        """
        calculate spotify chart score
        :param country: south-korea
        :param year: 2025
        :param week: 1
        :return:
        """
        if not country or not year or not week:
            raise ValueError("country, year and week are required")

        year = str(year)
        week = int(week)

        pipeline = [
            # match country / year / week
            {"$match": {
                "country": country,
                "year": year,
                "week": week,
            }},
            # keep only required fields
            {"$project": {
                "_id": 0,
                "datetime": 1,
                "country": 1,
                "year": 1,
                "month": 1,
                "day": 1,
                "week": 1,
                "weekly_top_songs": 1,
            }},
            # unwind songs
            {"$unwind": "$weekly_top_songs"},
            # calculate rank & score
            {"$project": {
                "datetime": 1,
                "year": 1,
                "month": 1,
                "day": 1,
                "week": 1,
                "country": 1,
                "sp_rank": {"$toInt": "$weekly_top_songs.rank"},
                "sp_song": "$weekly_top_songs.title",
                "sp_artist_id": "$weekly_top_songs.artist_id",
                "artist": {
                    "$trim": {
                        "input": "$weekly_top_songs.artist",
                        "chars": ","
                    }
                }
            }},
            # score = 201 - rank
            {"$addFields": {
                "sp_score": {
                    "$subtract": [201, "$sp_rank"]
                }
            }},
            # group by spotify artist id
            {"$group": {
                "_id": "$sp_artist_id",
                "datetime": {"$first": "$datetime"},
                "year": {"$first": "$year"},
                "month": {"$first": "$month"},
                "day": {"$first": "$day"},
                "week": {"$first": "$week"},
                "country": {"$first": "$country"},
                "artist": {"$first": "$artist"},
                "sp_score_list": {"$push": "$sp_score"},
            }},
            # sum score list
            {"$project": {
                "_id": 0,
                "spotify_id": "$_id",
                "datetime": 1,
                "year": 1,
                "month": 1,
                "day": 1,
                "week": 1,
                "country": 1,
                "artist": 1,
                "sp_chart_score": {
                    "$sum": "$sp_score_list"
                }
            }},
            # sort by score
            {"$sort": {"sp_chart_score": -1}}
        ]

        result = list(SpotifyCharts.objects.aggregate(pipeline))

        return result

    @staticmethod
    def get_trending_artist_ost_score(year, week):
        if not year or not week:
            raise ValueError("country, year and week are required")

        year = int(year)
        week = int(week)

        qs = (
            SpotifyOst.objects(year=year, week=week)
                .only(
                "year",
                "week",
                "datetime",
                "track",
                "track_code",
                "album",
                "album_code",
                "artist",
                "artist_code",
                "added_at",
                "country",
                "release_date",
                "popularity",
                "thumbnail",
                "play_counts",
            )
        )

        results = []
        for doc in qs:
            results.append({
                "year": doc.year,
                "week": doc.week,
                "datetime": doc.datetime,
                "track": doc.track,
                "track_code": doc.track_code,
                "album": doc.album,
                "album_code": doc.album_code,
                "artist": doc.artist,
                "artist_code": doc.artist_code,
                "added_at": doc.added_at,
                "country": doc.country,
                "release_date": doc.release_date,
                "popularity": doc.popularity,
                "thumbnail": doc.thumbnail,
                "play_counts": int(doc.play_counts) if doc.play_counts else 0
            })

        return results
