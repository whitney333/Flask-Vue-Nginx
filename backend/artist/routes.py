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

     return
    """
    def get_music_charts(self, country, week):
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
                #         "_all": {"$addToSet": "$$ROOT"},
                #             "mid": {"$addToSet": "$mid"},
                #             "artist": {"$addToSet": "$artist"},
                #             "sp_total_score": {"$addToSet": "$sp_total_score"},
                #         "mid": {"$push": "$mid"},
                #         # artist should be separated
                #         "artist": {"$push": "$artist"},
                #         "datetime": {"$first": "$datetime"},
                #         "year": {"$first": "$year"},
                #         "month": {"$first": "$month"},
                #         "day": {"$first": "$day"},
                #         "week": {"$first": "$week"},
                #         "country": {"$first": "$country"},
                #         # spotify score
                #         "sp_total_score": {"$first": "$sp_total_score"},
                #         "platforms": {"$first": "$platforms"},
                #         "youtube_week": {"$first": "$youtube_week"},
                #         "youtube_country": {"$first": "$youtube_country"},
                "yt_score": {"$addToSet": "$yt_score"},
                "yt_artist": {"$first": "$yt_charts_artist"}
            }}

            # match spotify-youtube artist with artist name
            #     {"$match": {
            #        # match artist name with youtube chart artist name
            #        "artist": "Jimin",
            #        "youtube_charts": {
            #           "$elemMatch": {
            #               "artist": "$youtube_charts.artist"
            #           }
            #        }
            #     }}
            #     {"$project": {
            #         "spotify_weekly_top_songs":
            #     }}

            #     {"$unwind": "$spotify_weekly_top_songs"},
            #     {"$project": {
            #         "datetime": "$datetime",
            #         "country": "$country",
            #         "year": "$year",
            #         "month": "$month",
            #         "day": "$day",
            #         "week": "$week",
            #     }}
            #     {"$project": {
            #        "combine": {
            #           "$concatArrays": [
            #               "$spotify_weekly_top_songs", "$youtube_weekly_top_songs"
            #            ]
            #        }
            #     }}
            #     {"$unwind": "$youtube_weekly_top_songs"},

        ])

    def get_instagram_latest_twelve(self):
        pass


