import datetime
import os
from pymongo import MongoClient
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

    def get(self):
        posts_data = reqparse.RequestParser()
        posts_data.add_argument('country', type=str, required=True, location='args')
        posts_data.add_argument('week', type=int, required=True, location='args')

        data = posts_data.parse_args()
        country = data['country']
        week = data['week']

        # get music, drama, sns score
        try:
            # test week:48, region: south korea
            drama_data = self.get_drama_score(country, week)
            music_data = self.get_music_score(country, week)
            sns_data = self.get_sns_score()

            return jsonify({'drama': drama_data,
                            'music': music_data,
                            'sns': sns_data})
        except Exception as e:
            return dumps({'err': str(e)})


    def get_artist(self):
        try:
            artist_results = general_db.Artist.aggregate([
                {"$sort": {"MID": 1}}
            ])
            obj_list = []
            for item in artist_results:
                obj_list.append(item)

            return jsonify(obj_list)
        except Exception as e:
            return dumps({'err': str(e)})

    def get_music_score(self, country, week):
        try:
            # stage 1: spotify charts
            # match country & week
            match_spotify = {
                "$match": {
                    "country": country,
                    "week": week
                }
            }

            # return fields
            project_spotify = {
                "$project": {
                    "_id": 0,
                    "datetime": "$datetime",
                    "country": "$country",
                    "year": "$year",
                    "month": "$month",
                    "day": "$day",
                    "week": "$week",
                    "spotify_weekly_top_songs": "$weekly_top_songs",
                }}

            # flatten weekly top songs
            unwind_spotify = {
                "$unwind": "$spotify_weekly_top_songs"
            }

            # preprocess fields and calculate spotify score
            calculate_score_spotify = {
                "$project": {
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
                }
            }

            # add field of spotify score
            add_score_spotify = {
                "$addFields": {
                    "sp_score": {
                        "$subtract": [
                            {"$toInt": 201},
                            {"$toInt": "$sp_rank"}
                        ]
                    }
                }
            }

            # group artist
            group_spotify = {
                "$group": {
                    "_id": "$sp_artist_id",
                    "datetime": {"$first": "$datetime"},
                    "year": {"$first": "$year"},
                    "month": {"$first": "$month"},
                    "day": {"$first": "$day"},
                    "week": {"$first": "$week"},
                    "country": {"$first": "$country"},
                    "artist": {"$first": "$artist"},
                    "sp_score_list": {"$addToSet": "$sp_score"}
                }
            }

            # return final fields
            get_final_spotify = {
                "$project": {
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
                }
            }

            # stage 2
            # lookup Artist collection to integrate artist basic info: music platforms & social media accounts
            lookup_artist = {
                "$lookup": {
                    "from": "Artist",
                    "localField": "sp_id",
                    "foreignField": "MUSIC_PLATFORMS.ID",
                    "as": "artist_info"
                }
            }

            first_project_artist = {
                "$project": {
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
                }
            }

            # concat music platforms & social media accounts
            concat_artist = {
                "$project": {
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
                }
            }

            # project final results of Artist info
            get_final_artist = {
                "$project": {
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
                }
            }

            # stage 3
            # lookup youtube charts
            lookup_youtube = {
                "$lookup": {
                    "from": "youtube_charts",
                    "localField": "week",
                    "foreignField": "week",
                    "as": "youtube_charts"
                }
            }

            # unwind youtube chart
            unwind_youtube = {
                "$unwind": "$youtube_charts"
            }

            # match relevant country
            match_country_youtube = {
                "$match": {"youtube_charts.country": "south korea"}
            }

            # return fields
            first_project_youtube = {
                "$project": {
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
                }
            }

            # convert youtube rank to integer
            second_project_youtube = {
                "$project": {
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
                }
            }

            # add new field, and calculate score of youtube chart by artist
            calculate_score_youtube = {
                "$addFields": {
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
                }
            }

            # unwind youtube chart
            second_unwind_youtube = {
                "$unwind": "$yt_charts"
            }

            # return expanded fields
            expand_value_youtube = {
                "$project": {
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
                }
            }

            # group by artist
            group_youtube = {
                "$group": {
                    "_id": "$yt_charts_artist",
                    "_all": {"$addToSet": "$$ROOT"},
                    "yt_score_list": {"$addToSet": "$yt_score"},
                    "yt_artist": {"$first": "$yt_charts_artist"}
                }
            }

            # calculate youtube total score
            calculate_total_score_youtube = {
                "$project": {
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
                }
            }

            # match youtube artist with spotify artist, if artist name is the same, keep it; not the same, drop it
            match_artist_youtube_with_spotify = {
                "$addFields": {
                    "_artist": {
                        "$filter": {
                            "input": "$_all",
                            "cond": {
                                "$eq": ["$$this.artist", "$$this.yt_charts_artist"]
                            }
                        }
                    }
                }
            }

            # return fields
            third_project_youtube = {
                "$project": {
                    "yt_artist": "$yt_artist",
                    "yt_total_score": "$yt_total_score",
                    "artist": {
                        "$arrayElemAt": ["$_artist", 0]
                    }
                }
            }

            # reutrn final reuslt of youtube
            get_final_youtube = {
                # organize artist info
                "$project": {
                    "mid": "$artist.mid",
                    "artist": "$artist.artist",
                    "week": "$artist.week",
                    "country": "$youtube_country",
                    "spotify_total_score": "$artist.sp_total_score",
                    "youtube_total_score": "$artist.yt_score",
                    "platforms": "$artist.platforms"
                }
            }

            # stage 4
            # lookup billboard global 200 chart
            lookup_billboard = {
                "$lookup": {
                    "from": "billboard_charts",
                    "localField": "week",
                    "foreignField": "week",
                    "as": "billboard_charts"
                }
            }

            # get billboard chart rank
            get_rank_billboard = {
                "$project": {
                    "mid": "$mid",
                    "artist": "$artist",
                    "week": "$week",
                    "spotify_total_score": "$spotify_total_score",
                    "youtube_total_score": "$youtube_total_score",
                    "platforms": "$platforms",
                    "billboard_charts": {
                        "$arrayElemAt": ["$billboard_charts.data", 0]
                    }
                }
            }

            # convert billboard rank from string to integer
            convert_rank_billboard = {
                "$project": {
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
                }
            }

            # calculate billboard chart score
            calculate_score_billboard = {
                "$addFields": {
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
                }
            }

            # flatter array
            flatten_billboard = {
                "$unwind": "$bb_charts"
            }

            # return expanded array
            first_project_billboard = {
                "$project": {
                    "mid": "$mid",
                    "artist": "$artist",
                    "week": "$week",
                    "spotify_total_score": "$spotify_total_score",
                    "youtube_total_score": "$youtube_total_score",
                    "platforms": "$platforms",
                    "bb_charts_artist": "$bb_charts.artist",
                    "bb_score": "$bb_charts.bb_score"
                }
            }

            # group billboard artist
            group_billboard = {
                "$group": {
                    "_id": "$bb_charts_artist",
                    "_all": {"$addToSet": "$$ROOT"},
                    "bb_score_list": {"$addToSet": "$bb_score"},
                    "bb_artist": {"$first": "$bb_charts_artist"}
                }
            }

            # calculate billboard total score
            calculate_total_score_billboard = {
                "$project": {
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
                }
            }

            # match billboard artist with artist
            # if text contains artist name, keep the value
            match_artist_billboard = {
                "$addFields": {
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
            }

            # sort score descending
            sort_score_billboard = {
                "$sort": {"bb_total_score": -1}
            }

            # return fields
            second_project_billboard = {
                "$project": {
                    "bb_artist": "$bb_artist",
                    "bb_total_score": "$bb_total_score",
                    "artist": {
                        "$arrayElemAt": ["$_artist", 0]
                    }
                }
            }

            third_project_billboard = {
                "$project": {
                    "mid": "$artist.mid",
                    "artist": "$artist.artist",
                    "week": "$artist.week",
                    "spotify_total_score": "$artist.spotify_total_score",
                    "youtube_total_score": "$artist.youtube_total_score",
                    "billboard_total_score": "$bb_total_score",
                    "platforms": "$artist.platforms"
                }
            }

            # match artist id
            match_artist_id_billboard = {
                "$match": {
                    "mid": {"$ne": None}
                }
            }

            # aggregate music score
            aggregate_music_score = {
                "$addFields": {
                    "music_performance_score": {
                        "$multiply": [
                            {"$add": ["$spotify_total_score", "$youtube_total_score", "$billboard_total_score"]}, 0.3
                        ]
                    }
                }
            }

            pipeline = [
                match_spotify,
                project_spotify,
                unwind_spotify,
                calculate_score_spotify,
                add_score_spotify,
                group_spotify,
                get_final_spotify,
                lookup_artist,
                first_project_artist,
                concat_artist,
                get_final_artist,
                lookup_youtube,
                unwind_youtube,
                match_country_youtube,
                first_project_youtube,
                second_project_youtube,
                calculate_score_youtube,
                second_unwind_youtube,
                expand_value_youtube,
                group_youtube,
                calculate_total_score_youtube,
                match_artist_youtube_with_spotify,
                third_project_youtube,
                get_final_youtube,
                lookup_billboard,
                get_rank_billboard,
                convert_rank_billboard,
                calculate_score_billboard,
                flatten_billboard,
                first_project_billboard,
                group_billboard,
                calculate_total_score_billboard,
                match_artist_billboard,
                sort_score_billboard,
                second_project_billboard,
                third_project_billboard,
                match_artist_id_billboard,
                aggregate_music_score
            ]

            results = general_db.spotify_charts.aggregate(pipeline)
            result = [item for item in results]

            return result
        except Exception as e:
            return dumps({'err': str(e)})

    def _get_sns_score(self):
        try:
            # stage 1
            # get tiktok index
            sort_tiktok = {"$sort": {"datetime": -1}}
            limit_tiktok = {"$limit": 1}
            project_tiktok = {"$project": {
                "datetime": "$datetime",
                "tiktok_hashtag_count": "$hashtag_count"
            }}

            # stage 2
            # lookup youtube index collection
            lookup_youtube = {
                "$lookup": {
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
                }
            }
            unwind_youtube = {"$unwind": "$youtube_index"}
            project_youtube = {
                "$project": {
                    "_id": 0,
                    "datetime": "$datetime",
                    "tiktok_hashtag_count": "$tiktok_hashtag_count",
                    "youtube_channel_id": "$youtube_index.channel_id",
                    "youtube_channel_hashtag_count": "$channel_hashtag",
                    "youtube_video_hashtag_count": "$video_hashtag"
                }}
            # stage 3
            # lookup instagram latest 12 posts
            lookup_instagram = {
                "$lookup": {
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
                }
            }

            unwind_instagram = {"$unwind": "$instagram_latest"}

            project_instagram = {
                "$project": {
                    "_id": 0,
                    "datetime": "$datetime",
                    "tiktok_hashtag_count": "$tiktok_hashtag_count",
                    "youtube_channel_id": "$youtube_channel_id",
                    "youtube_channel_hashtag_count": "$youtube_channel_hashtag_count",
                    "youtube_video_hashtag_count": "$youtube_video_hashtag_count",
                    "instagram_datetime": "$instagram_latest.date",
                    "instagram_follower_count": "$instagram_latest.follower_count",
                    "instagram_latest_posts": "$instagram_latest.post",
                }}

            group_result = {
                "$group": {
                    "_id": "$datetime",
                    "tiktok_hashtag_count": {"$first": "$tiktok_hashtag_count"},
                    "youtube_channel_id": {"$first": "$youtube_channel_id"},
                    "youtube_channel_hashtag_count": {"$first": "$youtube_channel_hashtag_count"},
                    "youtube_video_hashtag_count": {"$first": "$youtube_video_hashtag_count"},
                    "instagram_datetime": {"$push": "$instagram_datetime"},
                    "instagram_follower_count": {"$push": "$instagram_follower_count"},
                    "instagram_latest_posts": {"$last": "$instagram_latest_posts"}
                }}

            project_first_result = {
                "$project": {
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
                }}

            project_second_result = {
                "$project": {
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
                }}

            flatten_arr = {
                "$unwind": "$instagram_latest_posts"
            }

            preprocess = {
                "$project": {
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
                }}

            sum_insta_like_comment = {
                "$group": {
                    "_id": "$_id",
                    "tiktok_hashtag_count": {"$first": "$tiktok_hashtag_count"},
                    "youtube_channel_id": {"$first": "$youtube_channel_id"},
                    "youtube_channel_hashtag_count": {"$first": "$youtube_channel_hashtag_count"},
                    "youtube_video_hashtag_count": {"$first": "$youtube_video_hashtag_count"},
                    "instagram_follower_growth": {"$first": "$instagram_follower_growth"},
                    "instagram_total_likes": {"$sum": "$ig_like_count"},
                    "instagram_total_comments": {"$sum": "$ig_comment_count"}
                }}

            final_result = {
                "$project": {
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

            sort_final_result = {
                "$sort": {"datetime": -1},
            }

            limit_result = {"$limit": 1}

            pipeline = [
                sort_tiktok,
                limit_tiktok,
                project_tiktok,
                lookup_youtube,
                unwind_youtube,
                project_youtube,
                lookup_instagram,
                unwind_instagram,
                project_instagram,
                group_result,
                project_first_result,
                project_second_result,
                flatten_arr,
                preprocess,
                sum_insta_like_comment,
                final_result,
                sort_final_result,
                limit_result
            ]

            results = main_db.tiktok_index.aggregate(pipeline)
            result = [item for item in results]

            return result
        except Exception as e:
            return dumps({'err': str(e)})

    def get_drama_score(self):
        this_year = '{:02d}'.format(datetime.datetime.now().year)
        # str('{:02d}'.format(12))
        this_month = '{:02d}'.format(datetime.datetime.now().month)
        today = '{:02d}'.format(datetime.datetime.now().day)
        # week = datetime.date(int(this_year), int(this_month), int(today)).isocalendar()[1] - 1

        try:
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
                # match: south korea
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
                {"$match": {"week": 40}},
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
                    "total_streams": "$total_streams",
                    "nf_country": "$netflix_chart.country",
                    "nf_score":
                        {"$sum": [
                            {"$toInt": "$netflix_chart.rank_score"}, {"$toInt": "$netflix_chart.wkc_score"}
                        ]}
                }},
                {"$addFields": {
                    "drama_score": {
                        "$sum": ["$total_streams", "$nf_score"]
                    }
                }},
                {"$match": {"nf_country": "south-korea"}},
                {"$sort": {"drama_score": -1}}
            ])
            posts_list = []
            for item in results:
                posts_list.append(item)
            return posts_list
        except Exception as e:
            return dumps({'err': str(e)})

    def get_sns_score(self):
        try:
            #fetch artist_sns_score collection
            #stage 1
            get_data = {
                ""
            }

        except Exception as e:
            return dumps({'err': str(e)})

# Trending Artist
# trending-artist/rank/taiwan
# @artist_api_bp.route('/trending-artist/rank/taiwan')
# def get_trending_rank_taiwan():
#


# shows top 100 drama
class DramaScore(Resource):
    def get(self):
        posts_data = reqparse.RequestParser()
        posts_data.add_argument('region', type=str, required=True, location='args')
        posts_data.add_argument('week', type=int, required=True, location='args')

        data = posts_data.parse_args()
        region = data['region']
        week = data['week']
        _temp_list = []

        this_year = '{:02d}'.format(datetime.datetime.now().year)
        # str('{:02d}'.format(12))
        this_month = '{:02d}'.format(datetime.datetime.now().month)
        today = '{:02d}'.format(datetime.datetime.now().day)
        # week = datetime.date(int(this_year), int(this_month), int(today)).isocalendar()[1] - 1

        try:
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
                # match: south korea
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
                    "total_streams": "$total_streams",
                    "nf_country": "$netflix_chart.country",
                    "nf_score":
                        {"$sum": [
                            {"$toInt": "$netflix_chart.rank_score"}, {"$toInt": "$netflix_chart.wkc_score"}
                        ]}
                }},
                {"$addFields": {
                    "drama_score": {
                        "$sum": ["$total_streams", "$nf_score"]
                    }
                }},
                {"$match": {"nf_country": region}},
                {"$sort": {"drama_score": -1}},
                {"$limit": 100}
        ])
            posts_list = []
            for item in results:
                posts_list.append(item)
            return jsonify({'result': posts_list})
        except Exception as e:
            return dumps({'err': str(e)})

class CalculateSnsScore(Resource):
    pass
