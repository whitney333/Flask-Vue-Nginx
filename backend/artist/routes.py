import datetime

from flask import Flask, jsonify, request, Blueprint
from flask_cors import CORS
from random import randint
from models import main_db, general_db, campaign_db, spotify_week_db
from bson.json_util import dumps
from flask_restful import Resource, reqparse, Api


app = Flask(__name__)
CORS(app, resources={r'/*': {'origins': '*'}}, supports_credentials=True)

artist_api_bp = Blueprint('artist_api', __name__)
artist_api = Api(artist_api_bp)

@artist_api_bp.route('/artist/members', methods=['GET'])
def get_members_info():
    try:
        result = general_db.Artist.aggregate([
            {"$unwind": "$BELONG_GROUP_MID"},
            {"$match": {"BELONG_GROUP_MID": "1297"}},
            #TODO Return more details of the artist
            {"$project": {
                "_id": 0,
                "mid": "$MID",
                "artist": "$ARTIST_NAME",
                "name_in_korean": "$NAME_IN_KOREAN",
                "debut_year": "$DEBUT_YEAR",
                "nation": "$NATION",
                "type": "$TYPE",
                "belong_to": "$BELONG_GROUP_MID",
            }}
        ])
        return dumps({'result': result})
    except Exception as e:
        return dumps({'err': str(e)})

@artist_api_bp.route('/artist/campaign', methods=['GET'])
def get_campaign():
    try:
        results = campaign_db.campaign_package.aggregate([
            {"$match": {"MID": "1297"}},
            {"$project": {
                "_id": 0,
                "cid": "$CID",
                "mid": "$MID",
                "region": "$REGION",
                "language": "$LANGUAGE",
                "start_date": {
                    "$dateToString": {
                        "format": "%Y-%m-%d",
                        "date": "$START_DATE"
                    }
                },
                "cost": "$COST",
                "currency": "$CURRENCY",
                "posts": "$POSTS"
            }},
            {"$group": {
                "_id": "$cid",
                "cid": {"$first": "$cid"},
                "mid": {"$first": "$mid"},
                "start_date": {"$first": "$start_date"},
                "region": {"$push": "$posts.REGION"},
                "language": {"$addToSet": "$posts.LANGUAGE"},
                "budget": {"$first": "$cost"},
                "currency": {"$first": "currency"},
                "total_reach": {
                    "$sum": {"$sum": "$posts.FOLLOWER"}
                },
                "posts": {"$first": "$posts"}
            }},
            {"$unwind": "$region"},
            {'$addFields': {'region': {'$setUnion': ['$region', []]}}},
            {"$unwind": "$language"},
            {'$addFields': {'language': {'$setUnion': ['$language', []]}}}
        ])
        posts_list = []
        for item in results:
            posts_list.append(item)
        return dumps({'result': posts_list})
    except Exception as e:
        return str(e)

@artist_api_bp.route('/spotify/weekly-top-songs/<country>', methods=['GET'])
def get_spotify_weekly_top_songs(country):
    try:
        coll = spotify_week_db[country]
        # print(coll)
        results = coll.aggregate([
            {"$sort": {"datetime": -1}},
            {"$limit": 1},
            {"$project": {
                "_id": 0,
                "datetime": "$datetime",
                "year": "$year",
                "month": "$month",
                "day": "$day",
                "week": "$week",
                "weekly_top_songs": "$weekly_top_songs"
            }}
        ])
        return dumps({'result': results})
    except Exception as e:
        print(str(e))

class CampaignPackageDetail(Resource):
    def get(self):
        posts_data = reqparse.RequestParser()
        posts_data.add_argument('mid', type=str, required=True, location='args')
        posts_data.add_argument('cid', type=str, required=True, location='args')
        data = posts_data.parse_args()
        cid = data['cid']
        mid = data['mid']
        _temp_list = []

        try:
            fetch_posts = campaign_db.campaign_package.aggregate([
                {"$match": {"MID": mid}},
                {"$match": {"CID": cid}},
                {"$project": {
                    "_id": 0,
                    "cid": "$CID",
                    "mid": "$MID",
                    "region": "$REGION",
                    "language": "$LANGUAGE",
                    "start_date": {
                        "$dateToString": {
                            "format": "%Y-%m-%d",
                            "date": "$START_DATE"
                        }
                    },
                    "cost": "$COST",
                    "currency": "$CURRENCY",
                    "posts": "$POSTS"
                }},
                {"$group": {
                    "_id": "$cid",
                    "cid": {"$first": "$cid"},
                    "mid": {"$first": "$mid"},
                    "start_date": {"$first": "$start_date"},
                    "region": {"$push": "$posts.REGION"},
                    "language": {"$addToSet": "$posts.LANGUAGE"},
                    "budget": {"$first": "$cost"},
                    "currency": {"$first": "$currency"},
                    "total_reach": {
                        "$sum": {"$sum": "$posts.FOLLOWER"}
                    },
                    "posts": {"$first": "$posts"}
                }},
                {"$unwind": "$region"},
                {'$addFields': {'region': {'$setUnion': ['$region', []]}}},
                {"$unwind": "$language"},
                {'$addFields': {'language': {'$setUnion': ['$language', []]}}}
            ])
            posts_list = []
            for post in fetch_posts:
                posts_list.append(post)
            response = {'mid': mid,
                        'cid': cid,
                        'results': posts_list[0]}

            return jsonify(response)
        except Exception as e:
            return dumps({'err': str(e)})


class ArtistInfo(Resource):
    def get(self):
        posts_data = reqparse.RequestParser()
        posts_data.add_argument('mid', type=str, required=True, location='args')
        data = posts_data.parse_args()
        mid = data['mid']
        _temp_list = []

        try:
            result = general_db.Artist.aggregate([
                # MID is string data type
                {"$match": {"MID": mid}},
                {"$unwind": "$COMPANIES"},
                {"$project": {
                    "_id": 0,
                    "mid": "$MID",
                    "artist": "$ARTIST_NAME",
                    "name_in_korean": "$NAME_IN_KOREAN",
                    "debut_year": "$DEBUT_YEAR",
                    "debut_date": {
                        "$dateToString": {
                            "format": "%Y-%m-%d",
                            "date": "$DEBUT_DATE"
                        }},
                    "birth": {
                        "$dateToString": {
                            "format": "%Y-%m-%d",
                            "date": "$BIRTH"
                        }},
                    "nation": "$NATION",
                    "type": "$TYPE",
                    "belong_to": "$BELONG_GROUP_MID",
                    "labels": "$COMPANIES.COMPANY",
                    "fandom": "$FANDOM",
                    "color": "$COLOR",
                    "social_medias": "$SOCIAL_MEDIAS",
                    "music_plt": "$MUSIC_PLATFORMS",
                    "image": "$IMAGE"
                }}
            ])
            obj_list = []
            for item in result:
                obj_list.append(item)
            response = {'mid': mid,
                        'results': obj_list[0]}
            return jsonify(response)
        except Exception as e:
            return dumps({'err': str(e)})


class ArtistPopularity(Resource):
    """
     Calculate artist popularity
    :parameter: week, country
        (global, australia, brazil, canada, france, germany,
        hongkong, india, indonesia, italy, japan, malaysia,
        mexico, philippines, singapore, southkorea, spain,
        taiwan, thailand, unitedkingdom, usa, vietnam)
     return
    """

    def get_music_score(self, country, week):
        results = general_db.spotify_charts.aggregate([
            {"$match": {
                "country": "southkorea"
            }},
            {"$match": {"week": 35}},
            #     {"$unwind": "$weekly_top_songs"},
            {"$project": {
                "_id": 0,
                # spotify
                "datetime": "$datetime",
                "country": "$country",
                "year": "$year",
                "month": "$month",
                "day": "$day",
                "week": "$week",
                "spotify_weekly_top_songs": "$weekly_top_songs",
                #         "youtube_charts_id": "$youtube_charts._id",
                #         "youtube_week": "$youtube_charts.week",
                #         "youtube_weekly_top_songs": "$youtube_charts.weekly_top_songs"
            }},
            {"$unwind": "$spotify_weekly_top_songs"},
            # calculate spotify score
            {"$project": {
                "datetime": "$datetime",
                "year": "$year",
                "month": "$month",
                "day": "$day",
                "week": "$week",
                "country": "$country",
                "sp_rank": {"$toInt": "$spotify_weekly_top_songs.rank"},
                # check song title
                "sp_song": "$spotify_weekly_top_songs.title",
                "sp_artist_id": "$spotify_weekly_top_songs.artist_id",
                "artist": {
                    "$trim": {
                        "input": "$spotify_weekly_top_songs.artist",
                        "chars": ","
                    }
                }
            }},
            {"$addFields": {
                "sp_score": {
                    "$subtract": [
                        {"$toInt": 201},
                        {"$toInt": "$sp_rank"}
                    ]
                }
            }},
            # group by artist, get total score
            {"$group": {
                "_id": "$sp_artist_id",
                "datetime": {"$first": "$datetime"},
                "year": {"$first": "$year"},
                "month": {"$first": "$month"},
                "day": {"$first": "$day"},
                "week": {"$first": "$week"},
                "country": {"$first": "$country"},
                "artist": {"$first": "$artist"},
                "sp_score_list": {"$addToSet": "$sp_score"}
            }},
            {"$project": {
                "sp_id": "$_id",
                "datetime": "$datetime",
                "year": "$year",
                "month": "$month",
                "day": "$day",
                "week": "$week",
                "country": "$country",
                "artist": "$artist",
                "sp_total_score": {
                    "$reduce": {
                        "input": "$sp_score_list",
                        "initialValue": 0,
                        "in": {"$add": [{"$toInt": "$$value"}, "$$this"]}
                    }
                }
            }},
            # lookup artist
            {"$lookup": {
                "from": "Artist",
                "localField": "sp_id",
                "foreignField": "MUSIC_PLATFORMS.ID",
                "as": "artist_info"
            }},
            # return needed fields
            {"$project": {
                "sp_id": "$sp_id",
                "datetime": "$datetime",
                "year": "$year",
                "month": "$month",
                "day": "$day",
                "week": "$week",
                "country": "$country",
                "artist": "$artist",
                "sp_total_score": "$sp_total_score",
                "artist_mid": {
                    "$arrayElemAt": ["$artist_info.MID", 0]
                },
                "music_platforms": {
                    "$arrayElemAt": ["$artist_info.MUSIC_PLATFORMS", 0]
                },
                "social_medias": {
                    "$arrayElemAt": ["$artist_info.SOCIAL_MEDIAS", 0]
                }
            }},
            # concat music_platforms & social_medias
            {"$project": {
                "sp_id": "$sp_id",
                "datetime": "$datetime",
                "year": "$year",
                "month": "$month",
                "day": "$day",
                "week": "$week",
                "country": "$country",
                "artist": "$artist",
                "sp_total_score": "$sp_total_score",
                "mid": "$artist_mid",
                "all": {
                    "$concatArrays": ["$music_platforms", "$social_medias"]
                }
            }},
            {"$project": {
                "mid": "$mid",
                "artist": "$artist",
                "datetime": "$datetime",
                "year": "$year",
                "month": "$month",
                "day": "$day",
                "week": "$week",
                "country": "$country",
                "sp_total_score": "$sp_total_score",
                "platforms": {
                    "$reduce": {
                        "input": "$all",
                        "initialValue": {},
                        "in": {
                            "$mergeObjects": [
                                "$$value",
                                {
                                    "$switch": {
                                        "branches": [
                                            {
                                                "case": {"$eq": ["$$this.PLATFORM", "SPOTIFY"]},
                                                "then": {"spotify": "$$this.ID"}
                                            },
                                            {
                                                "case": {"$eq": ["$$this.PLATFORM", "INSTAGRAM"]},
                                                "then": {"instagram": "$$this.USER"}
                                            },
                                            {
                                                "case": {"$eq": ["$$this.PLATFORM", "YOUTUBE"]},
                                                "then": {"youtube": "$$this.USER"}
                                            },
                                            {
                                                "case": {"$eq": ["$$this.PLATFORM", "TWITTER"]},
                                                "then": {"twitter": "$$this.USER"}
                                            },
                                            {
                                                "case": {"$eq": ["$$this.PLATFORM", "TIKTOK"]},
                                                "then": {"tiktok": "$$this.USER"}
                                            },
                                            {
                                                "case": {"$eq": ["$$this.PLATFORM", "WEIBO"]},
                                                "then": {"weibo": "$$this.USER"}
                                            },
                                            {
                                                "case": {"$eq": ["$$this.PLATFORM", "BILIBILI"]},
                                                "then": {"bilibili": "$$this.USER"}
                                            },
                                            {
                                                "case": {"$eq": ["$$this.PLATFORM", "MELON"]},
                                                "then": {"melon": "$$this.ID"}
                                            },
                                            {
                                                "case": {"$eq": ["$$this.PLATFORM", "GENIE"]},
                                                "then": {"genie": "$$this.ID"}
                                            },
                                            {
                                                "case": {"$eq": ["$$this.PLATFORM", "QQ"]},
                                                "then": {"qq": "$$this.ID"}
                                            },
                                        ], "default": {}
                                    }}]
                        }}
                }
            }},
            # lookup youtube charts
            {"$lookup": {
                "from": "youtube_charts",
                "localField": "week",
                "foreignField": "week",
                "as": "youtube_charts"
            }},
            {"$unwind": "$youtube_charts"},
            {"$match": {"youtube_charts.country": "south korea"}},
            {"$project": {
                "mid": "$mid",
                "artist": "$artist",
                "datetime": "$datetime",
                "year": "$year",
                "month": "$month",
                "day": "$day",
                "week": "$week",
                "country": "$country",
                "sp_total_score": "$sp_total_score",
                "platforms": "$platforms",
                "youtube_week": "$youtube_charts.week",
                "youtube_country": "$youtube_charts.country",
                "youtube_charts": "$youtube_charts.weekly_top_songs"
            }},
            # convert yt_rank to integer
            {"$project": {
                "_id": 0,
                "mid": "$mid",
                "artist": "$artist",
                "datetime": "$datetime",
                "year": "$year",
                "month": "$month",
                "day": "$day",
                "week": "$week",
                "country": "$country",
                "sp_total_score": "$sp_total_score",
                "platforms": "$platforms",
                "youtube_week": "$youtube_week",
                "youtube_country": "$youtube_country",
                "yt_charts": {
                    "$map": {
                        "input": "$youtube_charts",
                        "as": "yt_item",
                        "in": {
                            "rank": {"$toInt": "$$yt_item.rank"},
                            "pre_rank": {"$toInt": "$$yt_item.previous_rank"},
                            "title": "$$yt_item.title",
                            "artist": "$$yt_item.artist",
                            "rank_position": "$$yt_item.rank_position"
                        }
                    }
                }
            }},
            # calculate youtube charts score by artists first
            {"$addFields": {
                "yt_charts": {
                    "$map": {
                        "input": "$yt_charts",
                        "as": "yt_chart",
                        "in": {
                            "$mergeObjects": [
                                "$$yt_chart",
                                {"yt_score": {
                                    "$subtract": [
                                        {"$toInt": 101},
                                        {"$toInt": "$$yt_chart.rank"}]
                                }}
                            ]
                        }
                    }
                }
            }},
            {"$unwind": "$yt_charts"},
            # return expand yt
            {"$project": {
                "mid": "$mid",
                "artist": "$artist",
                "datetime": "$datetime",
                "year": "$year",
                "month": "$month",
                "day": "$day",
                "week": "$week",
                "country": "$country",
                "sp_total_score": "$sp_total_score",
                "platforms": "$platforms",
                "youtube_week": "$youtube_week",
                "youtube_country": "$youtube_country",
                "yt_charts_artist": "$yt_charts.artist",
                "yt_score": "$yt_charts.yt_score"
            }},
            {"$group": {
                "_id": "$yt_charts_artist",
                "_all": {"$addToSet": "$$ROOT"},
                "yt_score_list": {"$addToSet": "$yt_score"},
                "yt_artist": {"$first": "$yt_charts_artist"}
            }},
            # calculate yt total score
            {"$project": {
                "_id": 0,
                "_all": "$_all",
                "yt_artist": "$yt_artist",
                "yt_total_score": {
                    "$reduce": {
                        "input": "$yt_score_list",
                        "initialValue": 0,
                        "in": {
                            "$add": [{"$toInt": "$$value"}, "$$this"]
                        }
                    }
                }
            }},
            # match yt_artist with sp_artist, if artist name is the same, keep it; not the same, drop it
            {"$addFields": {
                "_artist": {
                    "$filter": {
                        "input": "$_all",
                        "cond": {
                            "$eq": ["$$this.artist", "$$this.yt_charts_artist"]
                        }
                    }
                }
            }},
            {"$project": {
                "yt_artist": "$yt_artist",
                "yt_total_score": "$yt_total_score",
                "artist": {
                    "$arrayElemAt": ["$_artist", 0]
                }
            }},
            # organize artist info
            {"$project": {
                "mid": "$artist.mid",
                "artist": "$artist.artist",
                "week": "$artist.week",
                "country": "$youtube_country",
                "spotify_total_score": "$artist.sp_total_score",
                "youtube_total_score": "$artist.yt_score",
                "platforms": "$artist.platforms"
            }},
            # lookup billboard global 200
            {"$lookup": {
                "from": "billboard_charts",
                "localField": "week",
                "foreignField": "week",
                "as": "billboard_charts"
            }},
            # billboard ranking is global ranking
            {"$project": {
                "mid": "$mid",
                "artist": "$artist",
                "week": "$week",
                "spotify_total_score": "$spotify_total_score",
                "youtube_total_score": "$youtube_total_score",
                "platforms": "$platforms",
                "billboard_charts": {
                    "$arrayElemAt": ["$billboard_charts.data", 0]
                }
            }},
            # convert billboard rank to integer
            {"$project": {
                "mid": "$mid",
                "artist": "$artist",
                "week": "$week",
                "spotify_total_score": "$spotify_total_score",
                "youtube_total_score": "$youtube_total_score",
                "platforms": "$platforms",
                "bb_charts": {
                    "$map": {
                        "input": "$billboard_charts",
                        "as": "bb_item",
                        "in": {
                            "rank": {"$toInt": "$$bb_item.ranking"},
                            "artist": "$$bb_item.artist"
                        }
                    }
                }
            }},
            # calculate billboard charts score
            {"$addFields": {
                "bb_charts": {
                    "$map": {
                        "input": "$bb_charts",
                        "as": "bb_chart",
                        "in": {
                            "$mergeObjects": [
                                "$$bb_chart",
                                {"bb_score": {
                                    "$subtract": [
                                        {"$toInt": 201},
                                        "$$bb_chart.rank"
                                    ]
                                }}
                            ]
                        }
                    }
                }
            }},
            {"$unwind": "$bb_charts"},
            # return expanded billboard
            {"$project": {
                "mid": "$mid",
                "artist": "$artist",
                "week": "$week",
                "spotify_total_score": "$spotify_total_score",
                "youtube_total_score": "$youtube_total_score",
                "platforms": "$platforms",
                "bb_charts_artist": "$bb_charts.artist",
                "bb_score": "$bb_charts.bb_score"
            }},
            {"$group": {
                "_id": "$bb_charts_artist",
                "_all": {"$addToSet": "$$ROOT"},
                "bb_score_list": {"$addToSet": "$bb_score"},
                "bb_artist": {"$first": "$bb_charts_artist"}
            }},
            # calculate billboard total score
            {"$project": {
                "_id": 0,
                "_all": "$_all",
                "bb_artist": "$bb_artist",
                "bb_total_score": {
                    "$reduce": {
                        "input": "$bb_score_list",
                        "initialValue": 0,
                        "in": {
                            "$add": [{"$toInt": "$$value"}, "$$this"]
                        }
                    }
                }
            }},
            # match billboard artist with artist
            # if text contains artist name, keep the value
            {"$addFields": {
                "_artist": {
                    "$filter": {
                        "input": "$_all",
                        "as": "temp",
                        "cond": {
                            "$eq": ["$$temp.artist",
                                    "$$temp.bb_charts_artist"]
                        }
                    }
                }
            }
            },
            {"$sort": {"bb_total_score": -1}},
            # match artist
            {"$project": {
                "bb_artist": "$bb_artist",
                "bb_total_score": "$bb_total_score",
                "artist": {
                    "$arrayElemAt": ["$_artist", 0]
                }
            }},
            # return needed fields
            {"$project": {
                "mid": "$artist.mid",
                "artist": "$artist.artist",
                "week": "$artist.week",
                "spotify_total_score": "$artist.spotify_total_score",
                "youtube_total_score": "$artist.youtube_total_score",
                "billboard_total_score": "$bb_total_score",
                "platforms": "$artist.platforms"
            }},
            {"$match": {
                "mid": {"$ne": None}
            }},
            {"$addFields": {
                "music_performance_score": {
                    "$multiply": [
                        {"$add": ["$spotify_total_score", "$youtube_total_score", "$billboard_total_score"]}, 0.3
                    ]
                }
            }}
    ])

    def get_sns_score(self):
        results = general_db.tiktok_index.aggregate([
            {"$sort": {"datetime": -1}},
            {"$limit": 1},
            {"$project": {
                "datetime": "$datetime",
                "tiktok_hashtag_count": "$hashtag_count"
            }},
            # lookup youtube index collection with: date
            {"$lookup": {
                "from": "youtube_index",
                "let": {
                    "foreign_datetime": {
                        "$dateToString": {
                            "date": "$datetime",
                            "format": "%Y-%m-%d"
                        }
                    }},
                "pipeline": [
                    {"$match": {
                        "$expr": {
                            "$eq": [
                                "$$foreign_datetime",
                                {"$dateToString": {
                                    "date": "$datetime",
                                    "format": "%Y-%m-%d"
                                }}
                            ]
                        }
                    }}
                ],
                "as": "youtube_index"
            }},
            {"$unwind": "$youtube_index"},
            # return youtube needed fields
            {"$project": {
                "_id": 0,
                "datetime": "$datetime",
                "tiktok_hashtag_count": "$tiktok_hashtag_count",
                "youtube_channel_id": "$youtube_index.channel_id",
                "youtube_channel_hashtag_count": "$youtube_index.channel_hashtag",
                "youtube_video_hashtag_count": "$youtube_index.video_hashtag"
            }},
            # lookup instagram latest 12 posts
            {"$lookup": {
                "from": "instagram_latest",
                "let": {
                    "foreign_datetime": {
                        "$dateToString": {
                            "date": "$date",
                            "format": "%Y-%m-%d"
                        }
                    }},
                "pipeline": [
                    {"$match": {
                        "$expr": {
                            "$eq": [
                                "$$foreign_datetime",
                                {"$dateToString": {
                                    "date": "$datetime",
                                    "format": "%Y-%m-%d"
                                }}
                            ]
                        }
                    }}
                ],
                "as": "instagram_latest"
            }},
            {"$unwind": "$instagram_latest"},
            {"$project": {
                "_id": 0,
                "datetime": "$datetime",
                "tiktok_hashtag_count": "$tiktok_hashtag_count",
                "youtube_channel_id": "$youtube_channel_id",
                "youtube_channel_hashtag_count": "$youtube_channel_hashtag_count",
                "youtube_video_hashtag_count": "$youtube_video_hashtag_count",
                "instagram_datetime": "$instagram_latest.date",
                "instagram_follower_count": "$instagram_latest.follower_count",
                "instagram_latest_posts": "$instagram_latest.post",
            }},
            # group up by date
            {"$group": {
                "_id": "$datetime",
                "tiktok_hashtag_count": {"$first": "$tiktok_hashtag_count"},
                "youtube_channel_id": {"$first": "$youtube_channel_id"},
                "youtube_channel_hashtag_count": {"$first": "$youtube_channel_hashtag_count"},
                "youtube_video_hashtag_count": {"$first": "$youtube_video_hashtag_count"},
                "instagram_datetime": {"$push": "$instagram_datetime"},
                "instagram_follower_count": {"$push": "$instagram_follower_count"},
                "instagram_latest_posts": {"$last": "$instagram_latest_posts"}
            }},
            # return the first and the last element of follower count
            # calculate instagram 7-day follower change
            {"$project": {
                "tiktok_hashtag_count": "$tiktok_hashtag_count",
                "youtube_channel_id": "$youtube_channel_id",
                "youtube_channel_hashtag_count": "$youtube_channel_hashtag_count",
                "youtube_video_hashtag_count": "$youtube_video_hashtag_count",
                "instagram_the_first_follower_count": {
                    "$arrayElemAt": ["$instagram_follower_count", 0]
                },
                "instagram_the_last_follower_count": {
                    "$arrayElemAt": ["$instagram_follower_count", -1]
                },
                "instagram_latest_posts": "$instagram_latest_posts"
            }},
            {"$project": {
                "tiktok_hashtag_count": "$tiktok_hashtag_count",
                "youtube_channel_id": "$youtube_channel_id",
                "youtube_channel_hashtag_count": "$youtube_channel_hashtag_count",
                "youtube_video_hashtag_count": "$youtube_video_hashtag_count",
                "instagram_follower_growth": {
                    #             "$round": [
                    #                 {"$multiply": [
                    #                     {"$divide": [
                    "$subtract": ["$instagram_the_last_follower_count", "$instagram_the_first_follower_count"],
                    #                         "$instagram_the_first_follower_count"
                    #                     ]},
                    #                     100
                    #                 ]}, 3
                    #             ]
                },
                "instagram_latest_posts": "$instagram_latest_posts"
            }},
            # flatten array, and preprocess values
            {"$unwind": "$instagram_latest_posts"},
            {"$project": {
                "tiktok_hashtag_count": {"$toInt": "$tiktok_hashtag_count"},
                "youtube_channel_id": "$youtube_channel_id",
                "youtube_channel_hashtag_count": {
                    "$cond": {
                        "if": {
                            "$eq": ["$youtube_channel_hashtag_count", "< 100"]
                        },
                        "then": {"$toInt": 100},
                        "else": "$youtube_channel_hashtag_count"
                    }
                },
                "youtube_video_hashtag_count": {
                    "$cond": {
                        "if": {
                            "$eq": ["$youtube_video_hashtag_count", "< 100"]
                        },
                        "then": {"$toInt": 100},
                        "else": "$youtube_video_hashtag_count"
                    }
                },
                "instagram_follower_growth": "$instagram_follower_growth",
                "ig_like_count": {
                    "$cond": {
                        "if": {
                            "$lt": ["$instagram_latest_posts.like_count", 0]
                        },
                        "then": {"$toInt": 0},
                        "else": "$instagram_latest_posts.like_count"
                    }
                },
                "ig_comment_count": "$instagram_latest_posts.comment_count"
            }},
            # group by datetime, and sum up instagram likes & comments
            {"$group": {
                "_id": "$_id",
                "tiktok_hashtag_count": {"$first": "$tiktok_hashtag_count"},
                "youtube_channel_id": {"$first": "$youtube_channel_id"},
                "youtube_channel_hashtag_count": {"$first": "$youtube_channel_hashtag_count"},
                "youtube_video_hashtag_count": {"$first": "$youtube_video_hashtag_count"},
                "instagram_follower_growth": {"$first": "$instagram_follower_growth"},
                "instagram_total_likes": {"$sum": "$ig_like_count"},
                "instagram_total_comments": {"$sum": "$ig_comment_count"}
            }},
            {"$project": {
                "datetime": "$_id",
                "youtube_channel_id": "$youtube_channel_id",
                "sns_score": {
                    "$sum": ["$tiktok_hashtag_count",
                             "$youtube_channel_hashtag_count",
                             "$youtube_video_hashtag_count",
                             "$instagram_follower_count",
                             "$instagram_total_likes",
                             "$instagram_total_comments"]
                }
            }}
        ])

    def get_drama_score(self):
        this_year = '{:02d}'.format(datetime.datetime.now().year)
        # str('{:02d}'.format(12))
        this_month = '{:02d}'.format(datetime.datetime.now().month)
        today = '{:02d}'.format(datetime.datetime.now().day)
        week = datetime.date(int(this_year), int(this_month), int(today)).isocalendar()[1]-1

        results = general_db.Drama.aggregate([
            # match drama which are greater or equal than last year
            # and less or equal than next year
            {"$match": {
                "BROADCAST_YEAR": {
                    "$gte": int(this_year) - 1,
                    "$lte": int(this_year) + 1
                }
            }},
            # return needed fields
            {"$project": {
                "korean_name": "$NAME_IN_KOREAN",
                "english_name": "$NAME",
                "mid": "$STARRING.MID"
            }},
            # get spotify ost
            {"$lookup": {
                "from": "spotify_ost",
                "let": {"english_name": "$english_name"},
                "pipeline": [
                    {"$match": {
                        "$expr": {
                            "$regexMatch": {
                                "input": {"$toString": "$$english_name"},
                                "regex": ".*"
                            }
                        }
                    }}
                ],
                "as": "spotify_ost"
            }},
            # match country
            {"$unwind": "$spotify_ost"},
            {"$match": {"spotify_ost.country": "southkorea"}},
            # return needed fields
            {"$project": {
                "drama_korean_name": "$korean_name",
                "drama_english_name": "$english_name",
                "mid": "$mid",
                "week": "$spotify_ost.week",
                "datetime": "$spotify_ost.datetime",
                "country": "$spotify_ost.country",
                "album": "$spotify_ost.album",
                "artist": "$spotify_ost.artist",
                "artist_spotify_code": "$spotify_ost.artist_code",
                "popularity": "$spotify_ost.popularity",
                "play_counts": "$spotify_ost.play_counts"
            }},
            # match drama name with album name
            {"$addFields": {
                "is_match": {
                    "$regexMatch": {
                        "input": "$album",
                        "regex": {
                            "$concat": [".*", {"$toString": "$drama_english_name"}, ".*"]
                        },
                        "options": "i"
                    }
                }
            }},
            # match drama with album name
            {"$match": {"is_match": True}},
            # return needed fields
            {"$project": {
                "drama_korean_name": "$drama_korean_name",
                "drama_english_name": "$drama_english_name",
                "mid": "$mid",
                "week": "$week",
                "datetime": "$datetime",
                "country": "$country",
                "album": "$album",
                "artist": "$artist",
                "artist_spotify_code": "$artist_spotify_code",
                "popularity": "$popularity",
                "play_counts": "$play_counts",
                #         "is_match": "$is_match"
            }},
            # match week date
            {"$match": {"week": week}},
            # group by drama
            # keep artist mid, play counts of songs, week, datetime, country
            {"$group": {
                "_id": "$drama_english_name",
                "drama_korean_name": {"$first": "$drama_korean_name"},
                "mid": {"$first": "$mid"},
                "week": {"$first": "$week"},
                "datetime": {"$first": "$datetime"},
                "country": {"$addToSet": "$country"},
                "play_counts": {"$push": {"$toInt": "$play_counts"}}
            }},
            # calculate total streams each drama
            {"$project": {
                "_id": 1,
                "drama_korean_name": "$drama_korean_name",
                "mid": "$mid",
                "week": "$week",
                "datetime": "$datetime",
                "country": "$country",
                "total_streams": {"$sum": "$play_counts"}
            }},
            {"$unwind": "$country"},
            {"$sort": {"total_streams": -1}},
            # lookup netflix chary matching: week
            {"$lookup": {
                "from": "netflix_charts",
                "localField": "week",
                "foreignField": "week",
                "as": "netflix_chart"
            }},
            # match netflix drama name with the original drama name
            {"$addFields": {
                "_drama": {
                    "$filter": {
                        "input": "$netflix_chart",
                        "as": "netflix",
                        "cond": {
                            "$regexMatch": {
                                "input": {"$toString": "$$netflix.name"},
                                "regex": {
                                    "$concat": [".*", "$_id", ".*"]
                                },
                                "options": "i"
                            }
                        }
                    }
                }
            }},
            # return field
            {"$project": {
                "_id": 1,
                "drama_korean_name": "$drama_korean_name",
                "mid": "$mid",
                "week": "$week",
                "datetime": "$datetime",
                "sp_country": "$country",
                "total_streams": "$total_streams",
                "netflix_chart": "$_drama"
            }},
            {"$addFields": {
                "netflix_chart": {
                    "$map": {
                        "input": "$netflix_chart",
                        "as": "netflix_chart",
                        "in": {
                            "$mergeObjects": [
                                "$$netflix_chart",
                                {"rank_score": {
                                    "$subtract": [
                                        {"$toInt": 201},
                                        {"$toInt": "$$netflix_chart.rank"}
                                    ]
                                }}
                            ]
                        }
                    }
                }
            }},
            # calculate weeks on chart score
            {"$addFields": {
                "netflix_chart": {
                    "$map": {
                        "input": "$netflix_chart",
                        "as": "netflix_chart",
                        "in": {
                            "$mergeObjects": [
                                "$$netflix_chart",
                                {"wkc_score": {
                                    "$multiply": [
                                        {"$toInt": "$$netflix_chart.weeks_on_chart"}, 10
                                    ]
                                }}
                            ]
                        }
                    }
                }
            }},
            # match country: south-korea
            {"$unwind": "$netflix_chart"},
            #     {"$match": {"_drama.country": "south-korea"}},
            # return needed field
            {"$project": {
                "_id": 1,
                "drama_korean_name": "$drama_korean_name",
                "mid": "$mid",
                "week": "$week",
                "datetime": "$datetime",
                "sp_country": "$sp_country",
                "total_streams": "$total_streams",
                "nf_country": "$netflix_chart.country",
                "nf_score":
                    {"$sum": [
                        {"$toInt": "$netflix_chart.rank_score"}, {"$toInt": "$netflix_chart.wkc_score"}
                    ]}
            }}

        ])
