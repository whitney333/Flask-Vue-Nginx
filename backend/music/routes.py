from models import main_db, music_db, general_db, yt_db
from flask import jsonify, Blueprint
from bson.json_util import dumps
import datetime
from datetime import timedelta
from flask_restful import Resource, reqparse, Api
import re

music_api_bp = Blueprint('music_api', __name__)
music_api = Api(music_api_bp)

# add commas in number
def add_commas(number):
    return ("{:,}".format(number))

# remove commas in string
def rm_commas(string):
    return re.sub(",", "", string)

@music_api_bp.route('/spotify/top-city', methods=['GET'])
def get_spotify_top_city():
    try:
        result = main_db.spotify_info.aggregate([
            {"$sort": {"datetime": -1}},
            {"$limit": 1},
            {"$project": {
                "_id": 0,
                "date": {
                    "$dateToString": {
                        "format": "%Y-%m-%d",
                        "date": "$datetime"
                    }
                },
                "monthly_listeners": "$monthly_listeners",
                "top_city": "$top_country"
            }},
            {"$unwind": "$top_city"},
            {"$project": {
                "date": "$date",
                "monthly_listeners": "$monthly_listeners",
                "country": "$top_city.country",
                "city": "$top_city.city",
                "city_listener": {"$toInt": "$top_city.listener"}
            }},
            {"$project": {
                "date": "$date",
                "monthly_listeners": "$monthly_listeners",
                "country": "$country",
                "city": "$city",
                "city_listener": "$city_listener",
                "percentage": {"$round": [{"$divide": ["$city_listener", "$monthly_listeners"]}, 4]}
            }}
        ])
        return dumps({'result': result})
    except Exception as e:
        return dumps({'error': str(e)})


# @music_api_bp.route('/spotify/top-track/region', methods=['GET'])
# def get_spotify_top_track_by_region():
#     try:
#         result = main_db.spotify_info.aggregate([
#             {"$sort": {"datetime": -1}},
#             {"$limit": 1},
#             {"$project": {
#                 "_id": 0,
#                 "datetime": {
#                     "$dateToString": {
#                         "format": "%Y-%m-%d",
#                         "date": "$datetime"
#                     }
#                 },
#                 "top_track": "$top_track"
#             }},
#             {"$unwind": "$top_track"},
#             {"$project": {
#                 "_id": 0,
#                 "datetime": "$datetime",
#                 "region": "$top_track.region",
#                 "country": "$top_track.country",
#                 "tracks": "$top_track.tracks"
#             }},
#             {"$unwind": "$tracks"},
#             {"$project": {
#                 "_id": 0,
#                 "datetime": "$datetime",
#                 "country": "$country",
#                 "region": "$region",
#                 "top_track_name": "$tracks.track",
#                 "top_track_popularity": "$tracks.popularity"
#             }},
#             {"$sort": {"top_track_popularity": -1}},
#             {"$group": {
#                 "_id": {"region": "$region", "track": "$top_track_name"},
#                 "count": {"$sum": {"$toInt": 1}},
#                 "popularity": {"$sum": "$top_track_popularity"}
#             }},
#             {"$addFields": {
#                 "agg_popularity": {"$round": [{"$divide": ["$popularity", "$count"]}, 2]}
#             }},
#             {"$project": {
#                 "_id": 0,
#                 "region": "$_id.region",
#                 "track": "$_id.track",
#                 "count": "$count",
#                 "popularity": "$popularity",
#                 "agg_popularity": "$agg_popularity"
#             }},
#             {"$group": {
#                 "_id": "$track",
#                 "region": {"$push": "$region"},
#                 "agg_popularity": {"$push": "$agg_popularity"}
#             }},
#             {"$project": {
#                 "track_info": {
#                     "$map": {
#                         "input": {"$zip": {"inputs": ["$region", "$agg_popularity"]}},
#                         "in": {
#                             "region": {"$arrayElemAt": ["$$this", 0]},
#                             "agg_popularity": {"$arrayElemAt": ["$$this", 1]}
#                         }
#                     }
#                 }
#             }}
#         ])
#         return dumps({'result': result})
#     except Exception as e:
#         return dumps({'err': str(e)})

class TheShowMusicBroadcast(Resource):
    def get(self):
        posts_data = reqparse.RequestParser()
        posts_data.add_argument('year', type=int, required=True, location='args')
        posts_data.add_argument('week', type=int, required=True, location='args')
        data = posts_data.parse_args()
        year = data['year']
        week = data['week']

        fetch_posts = music_db.the_show.aggregate([
            {"$sort": {"onair_date": -1}},
            {"$match":
                 {"year":
                      {"$gt": year - 1,
                       "$lte": year}
                  }},
            {"$match": {
                "week":
                    {"$gt": week - 1,
                     "$lte": week}
            }},
            {"$project": {
                "_id": 0,
                "year": "$year",
                "week": "$week",
                "onair_date": "$onair_date",
                "artist": "$artist",
                "rank": "$rank",
                "song": "$song",
                "total_score": "$total_score"
            }}
        ])
        posts_list = []
        for post in fetch_posts:
            posts_list.append(post)
        response = {'year': year,
                    'week': week,
                    'result': posts_list}

        return jsonify(response)


class MusicCenterMusicBroadcast(Resource):
    def get(self):
        posts_data = reqparse.RequestParser()
        posts_data.add_argument('year', type=int, required=True, location='args')
        posts_data.add_argument('week', type=int, required=True, location='args')
        data = posts_data.parse_args()
        year = data['year']
        week = data['week']

        results = music_db.music_center.aggregate([
            {"$sort": {"datetime": -1}},
            {"$unwind": "$data"},
            {"$match":
                 {"year":
                      {"$lte": year,
                       "$gt": year - 1}
                  }
             },
            {"$match":
                 {"week":
                      {"$lte": week,
                       "$gt": week - 1}
                  }
             },
            {"$project": {
                "_id": 0,
                "week": "$week_date",
                "rank": "$data.rank",
                "artist": "$data.artist",
                "song": "$data.song",
                "soundtrack&AlbumScore": {
                    "$convert": {
                        "input": {
                            "$reduce": {
                                "input": {
                                    "$split": ["$data.sounrtrackAndAlbumScore", ',']
                                },
                                "initialValue": '',
                                "in": {
                                    "$concat": ['$$value', '$$this']
                                }
                            }
                        },
                        "to": 'int',
                        "onError": 0
                    }},
                "videoAndBroadcastScore": {
                    "$convert": {
                        "input": {
                            "$reduce": {
                                "input": {
                                    "$split": ["$data.videoAndBroadcastScore", ',']
                                },
                                "initialValue": '',
                                "in": {
                                    "$concat": ['$$value', '$$this']
                                }
                            }
                        },
                        "to": 'int',
                        "onError": 0
                    }},
                "previousVoteAndGlobal": {
                    "$convert": {
                        "input": {
                            "$reduce": {
                                "input": {
                                    "$split": ["$data.previousVoteAndGlobal", ',']
                                },
                                "initialValue": '',
                                "in": {
                                    "$concat": ['$$value', '$$this']
                                }
                            }
                        },
                        "to": 'int',
                        "onError": 0
                    }},
                "smsScore": {
                    "$convert": {
                        "input": {
                            "$reduce": {
                                "input": {
                                    "$split": ["$data.smsScore", ',']
                                },
                                "initialValue": '',
                                "in": {
                                    "$concat": ['$$value', '$$this']
                                }
                            }
                        },
                        "to": 'int',
                        "onError": 0
                    }},
                "totalScore": {
                    "$convert": {
                        "input": {
                            "$reduce": {
                                "input": {
                                    "$split": ["$data.totalScore", ',']
                                },
                                "initialValue": '',
                                "in": {
                                    "$concat": ['$$value', '$$this']
                                }
                            }
                        },
                        "to": 'int',
                        "onError": 0
                    }}
            }},
            {"$project": {
                "_id": 0,
                "week": "$week",
                "rank": "$rank",
                "artist": "$artist",
                "song": "$song",
                "soundtrack_album_score": "$soundtrack&AlbumScore",
                "total_score": "$totalScore",
                "video_broadcast_score": "$videoAndBroadcastScore",
                "global_vote_score": "$previousVoteAndGlobal",
                "sms_score": "$smsScore",
                "all_other_score": {
                    "$subtract": ["$totalScore", "$soundtrack&AlbumScore"]
                }
            }}
        ])

        posts_list = []
        for post in results:
            posts_list.append(post)
        response = {'year': year,
                    'week': week,
                    'result': posts_list}

        return jsonify(response)


class McountdownMusicBroadcast(Resource):
    def get(self):
        posts_data = reqparse.RequestParser()
        posts_data.add_argument('year', type=int, required=True, location='args')
        posts_data.add_argument('week', type=int, required=True, location='args')
        data = posts_data.parse_args()
        year = data['year']
        week = data['week']

        results = music_db.mcountdown.aggregate([
            {"$sort": {"datetime": -1}},
            {"$unwind": "$data"},
            {"$match":
                 {"year":
                      {"$lte": year,
                       "$gt": year - 1}
                  }
             },
            {"$match":
                 {"week":
                      {"$lte": week,
                       "$gt": week - 1}
                  }
             },
            {"$project": {
                "_id": 0,
                "week": "$week_date",
                "title": "$data.songName",
                "album": "$data.albumName",
                "artist": "$data.artistName",
                "soundScore": {"$toInt": "$data.soundScore"},
                "albumScore": {"$toInt": "$data.albumScore"},
                "globalSNS": {"$toInt": "$data.globalSNS"},
                "globalVote": {"$toInt": "$data.globalVote"},
                "broadcastScore": {"$toInt": "$data.broadcastScore"},
                "liveVote": {"$toInt": "$data.liveVote"},
                "totalScore": {"$toInt": "$data.totalScore"}
            }}
        ])


        posts_list = []
        for post in results:
            posts_list.append(post)
        response = {'year': year,
                    'week': week,
                    'result': posts_list}

        return jsonify(response)


class ShowChampionMusicBroadcast(Resource):
    def get(self):
        posts_data = reqparse.RequestParser()
        posts_data.add_argument('year', type=int, required=True, location='args')
        posts_data.add_argument('week', type=int, required=True, location='args')
        data = posts_data.parse_args()
        year = data['year']
        week = data['week']

        results = music_db.show_champion.aggregate([
            {"$sort": {"datetime": -1}},
            {"$unwind": "$data"},
            {"$match":
                 {"year":
                      {"$lte": year,
                       "$gt": year - 1}
                  }
            },
            {"$match":
                 {"week":
                      {"$lte": week,
                       "$gt": week - 1}
                  }
            },
            {"$project": {
                "_id": 0,
                "week": "$week_date",
                "rank": "$data.rank",
                "artist": "$data.artist",
                "song": "$data.song",
                "soundtrackScore": {"$toInt": "$data.soundtrackRank"},
                "albumScore": {"$toInt": "$data.albumRank"},
                "snsScore": {"$toInt": "$data.snsRank"},
                "globalFanScore": {"$toInt": "$data.globalFanRank"},
                "broadcastScore": {"$toInt": "$data.broadcastRank"},
                "totalScore": {"$toInt": "$data.totalScore"}
            }}
        ])

        posts_list = []
        for post in results:
            posts_list.append(post)
        response = {'year': year,
                    'week': week,
                    'result': posts_list}

        return jsonify(response)


class InkigayoMusicBroadcast(Resource):
    def get(self):
        posts_data = reqparse.RequestParser()
        posts_data.add_argument('year', type=int, required=True, location='args')
        posts_data.add_argument('week', type=int, required=True, location='args')
        data = posts_data.parse_args()
        year = data['year']
        week = data['week']

        results = music_db.inkigayo.aggregate([
            {"$sort": {"datetime": -1}},
            {"$match":
                 {"year":
                      {"$lte": year,
                       "$gt": year - 1}
                  }
             },
            {"$match":
                 {"week":
                      {"$lte": week,
                       "$gt": week - 1}
                  }
             },
            {"$unwind": "$data"},
            {"$project": {
                "_id": 0,
                "rank": {"$toInt": "$data.rank"},
                "artist": "$data.artist",
                "song": "$data.song",
                "soundtrackScore": {"$toInt": "$data.soundtrackScore"},
                "albumScore": {"$toInt": "$data.albumScore"},
                "snsScore": {"$toInt": "$data.snsScore"},
                "onairScore": {"$trim":
                                   {"input": "$data.onairScore"}
                               },
                "smsScore": {"$trim":
                                 {"input": "$data.smsScore"}
                             },
                "realtimeAppVoteScore": {"$toInt": "$data.realtimeAppVoteScore"}
            }},
            {"$project": {
                "_id": 0,
                "rank": "$rank",
                "artist": "$artist",
                "song": "$song",
                "soundtrackScore": "$soundtrackScore",
                "albumScore": "$albumScore",
                "snsScore": "$snsScore",
                "onairScore": {"$toInt": "$onairScore"},
                "smsScore": {"$toInt": "$smsScore"},
                "realtimeAppVoteScore": "$realtimeAppVoteScore"
            }}
        ])

        posts_list = []
        for post in results:
            posts_list.append(post)
        response = {'year': year,
                    'week': week,
                    'result': posts_list}

        return jsonify(response)


class SpotifyIndex(Resource):
    def get(self):
        posts_data = reqparse.RequestParser()
        posts_data.add_argument('end', type=lambda x: datetime.datetime.strptime(x, '%Y-%m-%d'), required=True,
                                location='args')
        posts_data.add_argument('range', type=str, required=True, location='args')
        data = posts_data.parse_args()
        end = data['end']
        range = data['range']

        _temp_list = []

        # Total number of posts
        posts_count_cur = main_db.spotify_info.aggregate([
            {"$sort": {"datetime": -1}},
            {"$group": {
                "_id": "total",
                "count": {"$sum": {"$toInt": 1}}
            }}
        ])

        for item in posts_count_cur:
            _temp_list.append(item['count'])

        posts_count = _temp_list[0]

        today_date = datetime.datetime.now()
        # month_date = datetime.datetime.now() - timedelta(days=30)
        # Specific date range for querying db: 1M/ 3M/ 6M/ 1Y/ Overall
        # Case 1:
        if (range == 'month'):
            fetch_posts = main_db.spotify_info.aggregate([
                {"$sort": {"datetime": -1}},
                {"$match":
                     {"datetime":
                          {"$lte": end,
                           "$gt": end - datetime.timedelta(days=30)}
                      }},
                {"$project": {
                    "_id": 0,
                    "date": {
                        "$dateToString": {
                            "format": "%Y-%m-%d",
                            "date": "$datetime"
                        }
                    },
                    "follower": "$followers",
                    "listener": "$monthly_listeners",
                    "popularity": "$popularity",
                    "conversion_rate": {
                        "$round": [{"$multiply": [{"$divide": ["$followers", "$monthly_listeners"]}, 100]}, 2]
                    },
                }},
                {"$sort": {"date": 1}}
            ])
            posts_list = []
            for post in fetch_posts:
                posts_list.append(post)
            response = {'total_posts_count': posts_count,
                        'range': range,
                        'end': end.strftime("%Y-%m-%d"),
                        'posts': posts_list}

            return jsonify(response)
        elif (range == 'three_month'):
            fetch_posts = main_db.spotify_info.aggregate([
                {"$sort": {"datetime": -1}},
                {"$match":
                     {"datetime":
                          {"$lte": end,
                           "$gt": end - datetime.timedelta(days=90)}
                      }},
                {"$project": {
                    "_id": 0,
                    "date": {
                        "$dateToString": {
                            "format": "%Y-%m-%d",
                            "date": "$datetime"
                        }
                    },
                    "follower": "$followers",
                    "listener": "$monthly_listeners",
                    "popularity": "$popularity",
                    "conversion_rate": {
                        "$round": [{"$multiply": [{"$divide": ["$followers", "$monthly_listeners"]}, 100]}, 2]
                    }
                }},
                {"$sort": {"date": 1}}
            ])
            posts_list = []
            for post in fetch_posts:
                posts_list.append(post)
            response = {'total_posts_count': posts_count,
                        'range': range,
                        'end': end.strftime("%Y-%m-%d"),
                        'posts': posts_list}

            return jsonify(response)
        elif (range == 'six_month'):
            fetch_posts = main_db.spotify_info.aggregate([
                {"$sort": {"datetime": -1}},
                {"$match":
                     {"datetime":
                          {"$lte": end,
                           "$gt": end - datetime.timedelta(days=180)}
                      }},
                {"$project": {
                    "_id": 0,
                    "date": {
                        "$dateToString": {
                            "format": "%Y-%m-%d",
                            "date": "$datetime"
                        }
                    },
                    "follower": "$followers",
                    "listener": "$monthly_listeners",
                    "popularity": "$popularity",
                    "conversion_rate": {
                        "$round": [{"$multiply": [{"$divide": ["$followers", "$monthly_listeners"]}, 100]}, 2]
                    }
                }},
                {"$sort": {"date": 1}}
            ])
            posts_list = []
            for post in fetch_posts:
                posts_list.append(post)
            response = {'total_posts_count': posts_count,
                        'range': range,
                        'end': end.strftime("%Y-%m-%d"),
                        'posts': posts_list}

            return jsonify(response)
        elif (range == 'year'):
            fetch_posts = main_db.spotify_info.aggregate([
                {"$sort": {"datetime": -1}},
                {"$match":
                     {"datetime":
                          {"$lte": end,
                           "$gt": end - datetime.timedelta(days=365)}
                      }},
                {"$project": {
                    "_id": 0,
                    "date": {
                        "$dateToString": {
                            "format": "%Y-%m-%d",
                            "date": "$datetime"
                        }
                    },
                    "follower": "$followers",
                    "listener": "$monthly_listeners",
                    "popularity": "$popularity",
                    "conversion_rate": {
                        "$round": [{"$multiply": [{"$divide": ["$followers", "$monthly_listeners"]}, 100]}, 2]
                    }
                }},
                {"$sort": {"date": 1}}
            ])
            posts_list = []
            for post in fetch_posts:
                posts_list.append(post)
            response = {'total_posts_count': posts_count,
                        'range': range,
                        'end': end.strftime("%Y-%m-%d"),
                        'posts': posts_list}

            return jsonify(response)
        elif (range == 'overall'):
            fetch_posts = main_db.spotify_info.aggregate([
                {"$sort": {"datetime": -1}},
                {"$match":
                     {"datetime":
                          {"$lte": end}
                      }},
                {"$project": {
                    "_id": 0,
                    "date": {
                        "$dateToString": {
                            "format": "%Y-%m-%d",
                            "date": "$datetime"
                        }
                    },
                    "follower": "$followers",
                    "listener": "$monthly_listeners",
                    "popularity": "$popularity",
                    "conversion_rate": {
                        "$round": [{"$multiply": [{"$divide": ["$followers", "$monthly_listeners"]}, 100]}, 2]
                    }
                }},
                {"$sort": {"date": 1}}
            ])
            posts_list = []
            for post in fetch_posts:
                posts_list.append(post)
            response = {'total_posts_count': posts_count,
                        'range': range,
                        'end': end.strftime("%Y-%m-%d"),
                        'posts': posts_list}

            return jsonify(response)
        else:
            fetch_posts = main_db.spotify_info.aggregate([
                {"$sort": {"datetime": -1}},
                {"$match":
                     {"datetime":
                          {"$lte": end,
                           "$gt": end - datetime.timedelta(days=30)}
                      }},
                {"$project": {
                    "_id": 0,
                    "date": {
                        "$dateToString": {
                            "format": "%Y-%m-%d",
                            "date": "$datetime"
                        }
                    },
                    "follower": "$followers",
                    "listener": "$monthly_listeners",
                    "popularity": "$popularity",
                    "conversion_rate": {
                        "$round": [{"$multiply": [{"$divide": ["$followers", "$monthly_listeners"]}, 100]}, 2]
                    }
                }},
                {"$sort": {"date": 1}}
            ])
            posts_list = []
            for post in fetch_posts:
                posts_list.append(post)
            response = {'total_posts_count': posts_count,
                        'range': range,
                        'end': end.strftime("%Y-%m-%d"),
                        'posts': posts_list}

            return jsonify(response)


class MelonFollower(Resource):
    def get(self):
        posts_data = reqparse.RequestParser()
        posts_data.add_argument('end', type=lambda x: datetime.datetime.strptime(x, '%Y-%m-%d'), required=True,
                                location='args')
        posts_data.add_argument('range', type=str, required=True, location='args')
        data = posts_data.parse_args()
        end = data['end']
        range = data['range']

        _temp_list = []

        # Total number of posts
        posts_count_cur = main_db.melon_follower.aggregate([
            {"$sort": {"datetime": -1}},
            {"$group": {
                "_id": "total",
                "count": {"$sum": {"$toInt": 1}}
            }}
        ])

        for item in posts_count_cur:
            _temp_list.append(item['count'])

        posts_count = _temp_list[0]

        today_date = datetime.datetime.now()
        # month_date = datetime.datetime.now() - timedelta(days=30)
        # Specific date range for querying db: 1M/ 3M/ 6M/ 1Y/ Overall
        # Case 1:
        if (range == 'month'):
            fetch_posts = main_db.melon_follower.aggregate([
                {"$sort": {"datetime": -1}},
                {"$match":
                     {"datetime":
                          {"$lte": end,
                           "$gt": end - datetime.timedelta(days=30)}
                      }},
                {"$project": {
                    "_id": 0,
                    "date": {
                        "$dateToString": {
                            "format": "%Y-%m-%d",
                            "date": "$datetime"
                        }
                    },
                    "follower": "$data.follower"
                }},
                {"$sort": {"date": 1}}
            ])
            posts_list = []
            for post in fetch_posts:
                posts_list.append(post)
            response = {'total_posts_count': posts_count,
                        'range': range,
                        'end': end.strftime("%Y-%m-%d"),
                        'posts': posts_list}

            return jsonify(response)

        elif (range == 'three_month'):
            fetch_posts = main_db.melon_follower.aggregate([
                {"$sort": {"datetime": -1}},
                {"$match":
                     {"datetime":
                          {"$lte": end,
                           "$gt": end - datetime.timedelta(days=90)}
                      }},
                {"$project": {
                    "_id": 0,
                    "date": {
                        "$dateToString": {
                            "format": "%Y-%m-%d",
                            "date": "$datetime"
                        }
                    },
                    "follower": "$data.follower"
                }},
                {"$sort": {"date": 1}}
            ])
            posts_list = []
            for post in fetch_posts:
                posts_list.append(post)
            response = {'total_posts_count': posts_count,
                        'range': range,
                        'end': end.strftime("%Y-%m-%d"),
                        'posts': posts_list}

            return jsonify(response)
        elif (range == 'six_month'):
            fetch_posts = main_db.melon_follower.aggregate([
                {"$sort": {"datetime": -1}},
                {"$match":
                     {"datetime":
                          {"$lte": end,
                           "$gt": end - datetime.timedelta(days=180)}
                      }},
                {"$project": {
                    "_id": 0,
                    "date": {
                        "$dateToString": {
                            "format": "%Y-%m-%d",
                            "date": "$datetime"
                        }
                    },
                    "follower": "$data.follower"
                }},
                {"$sort": {"date": 1}}
            ])
            posts_list = []
            for post in fetch_posts:
                posts_list.append(post)
            response = {'total_posts_count': posts_count,
                        'range': range,
                        'end': end.strftime("%Y-%m-%d"),
                        'posts': posts_list}

            return jsonify(response)
        elif (range == 'year'):
            fetch_posts = main_db.melon_follower.aggregate([
                {"$sort": {"datetime": -1}},
                {"$match":
                     {"datetime":
                          {"$lte": end,
                           "$gt": end - datetime.timedelta(days=365)}
                      }},
                {"$project": {
                    "_id": 0,
                    "date": {
                        "$dateToString": {
                            "format": "%Y-%m-%d",
                            "date": "$datetime"
                        }
                    },
                    "follower": "$data.follower"
                }},
                {"$sort": {"date": 1}}
            ])
            posts_list = []
            for post in fetch_posts:
                posts_list.append(post)
            response = {'total_posts_count': posts_count,
                        'range': range,
                        'end': end.strftime("%Y-%m-%d"),
                        'posts': posts_list}

            return jsonify(response)
        elif (range == 'overall'):
            fetch_posts = main_db.melon_follower.aggregate([
                {"$sort": {"datetime": -1}},
                {"$match":
                     {"datetime":
                          {"$lte": end}
                      }},
                {"$project": {
                    "_id": 0,
                    "date": {
                        "$dateToString": {
                            "format": "%Y-%m-%d",
                            "date": "$datetime"
                        }
                    },
                    "follower": "$data.follower"
                }},
                {"$sort": {"date": 1}}
            ])
            posts_list = []
            for post in fetch_posts:
                posts_list.append(post)
            response = {'total_posts_count': posts_count,
                        'range': range,
                        'end': end.strftime("%Y-%m-%d"),
                        'posts': posts_list}

            return jsonify(response)
        else:
            fetch_posts = main_db.melon_follower.aggregate([
                {"$sort": {"datetime": -1}},
                {"$match":
                     {"datetime":
                          {"$lte": end,
                           "$gt": end - datetime.timedelta(days=30)}
                      }},
                {"$project": {
                    "_id": 0,
                    "date": {
                        "$dateToString": {
                            "format": "%Y-%m-%d",
                            "date": "$datetime"
                        }
                    },
                    "follower": "$followers",
                    "listener": "$monthly_listeners",
                    "popularity": "$popularity",
                    "conversion_rate": {
                        "$round": [{"$multiply": [{"$divide": ["$followers", "$monthly_listeners"]}, 100]}, 2]
                    }
                }},
                {"$sort": {"date": 1}}
            ])
            posts_list = []
            for post in fetch_posts:
                posts_list.append(post)
            response = {'total_posts_count': posts_count,
                        'range': range,
                        'end': end.strftime("%Y-%m-%d"),
                        'posts': posts_list}

            return jsonify(response)


class WeeklyMusicCharts(Resource):
    def get(self):
        posts_data = reqparse.RequestParser()
        posts_data.add_argument('year', type=int, required=True, location='args')
        posts_data.add_argument('week', type=int, required=True, location='args')
        posts_data.add_argument('pl', type=str, required=True, location='args')
        data = posts_data.parse_args()
        year = data['year']
        week = data['week']
        pl = data['pl']

        _spotify_temp_list = []
        _melon_temp_list = []
        _genie_temp_list = []
        _qq_temp_list = []
        _billboard_temp_list = []
        _youtube_temp_list = []

        # Total number of posts of each platform
        posts_count_cur_spotify = music_db.week_chart_spotify.aggregate([
            {"$sort": {"datetime": -1}},
            {"$group": {
                "_id": "total",
                "count": {"$sum": {"$toInt": 1}}
            }}
        ])
        posts_count_cur_melon = music_db.week_chart_melon.aggregate([
            {"$sort": {"datetime": -1}},
            {"$group": {
                "_id": "total",
                "count": {"$sum": {"$toInt": 1}}
            }}
        ])
        posts_count_cur_genie = music_db.week_chart_genie.aggregate([
            {"$sort": {"datetime": -1}},
            {"$group": {
                "_id": "total",
                "count": {"$sum": {"$toInt": 1}}
            }}
        ])
        posts_count_cur_qq = music_db.week_chart_qq.aggregate([
            {"$sort": {"datetime": -1}},
            {"$group": {
                "_id": "total",
                "count": {"$sum": {"$toInt": 1}}
            }}
        ])
        posts_count_cur_youtube = music_db.week_chart_youtube.aggregate([
            {"$sort": {"datetime": -1}},
            {"$group": {
                "_id": "total",
                "count": {"$sum": {"$toInt": 1}}
            }}
        ])
        posts_count_cur_billboard = music_db.week_chart_billboard_global_two_hundred.aggregate([
            {"$sort": {"datetime": -1}},
            {"$group": {
                "_id": "total",
                "count": {"$sum": {"$toInt": 1}}
            }}
        ])

        for item in posts_count_cur_spotify:
            _spotify_temp_list.append(item['count'])
        posts_count_spotify = _spotify_temp_list[0]

        for item in posts_count_cur_melon:
            _melon_temp_list.append(item['count'])
        posts_count_melon = _melon_temp_list[0]

        for item in posts_count_cur_genie:
            _genie_temp_list.append(item['count'])
        posts_count_genie = _genie_temp_list[0]

        for item in posts_count_cur_qq:
            _qq_temp_list.append(item['count'])
        posts_count_qq = _qq_temp_list[0]

        for item in posts_count_cur_youtube:
            _youtube_temp_list.append(item['count'])
        posts_count_youtube = _youtube_temp_list[0]

        for item in posts_count_cur_billboard:
            _billboard_temp_list.append(item['count'])
        posts_count_billboard = _billboard_temp_list[0]

        # Case 1: Spotify
        if (pl == 'spotify'):
            fetch_posts = music_db.week_chart_spotify.aggregate([
                {"$sort": {"datetime": -1}},
                {"$match":
                     {"year":
                          {"$gt": year - 1,
                           "$lte": year}
                      }},
                {"$match": {
                    "week":
                        {"$gt": week - 1,
                         "$lte": week}
                }},
                {"$unwind": "$data"},
                {"$project": {
                    "_id": 0,
                    "year": "$year",
                    "week": "$week",
                    "artist": "$data.artist",
                    "peak": "$data.peak",
                    "rank": "$data.rank",
                    "rank_change": "$data.rank_change",
                    "streak": "$data.streak",
                    "streams": "$data.streams",
                    "title": "$data.title"
                }}
            ])
            posts_list = []
            for post in fetch_posts:
                posts_list.append(post)
            response = {'total_posts_count': posts_count_spotify,
                        'year': year,
                        'week': week,
                        'posts': posts_list,
                        'platform': 'spotify'}

            return jsonify(response)
        elif (pl == 'melon'):
            fetch_posts = music_db.week_chart_melon.aggregate([
                {"$sort": {"datetime": -1}},
                {"$match":
                     {"year":
                          {"$gt": year - 1,
                           "$lte": year}
                      }},
                {"$match": {
                    "week":
                        {"$gt": week - 1,
                         "$lte": week}
                }},
                {"$unwind": "$data"},
                {"$project": {
                    "_id": 0,
                    "year": "$ year",
                    "week": "$week",
                    "artist": "$data.artist",
                    "rank": "$data.ranking",
                    "rank_change": "$data.rank_position",
                    "title": "$data.title"
                }}
            ])
            posts_list = []
            for post in fetch_posts:
                posts_list.append(post)
            response = {'total_posts_count': posts_count_melon,
                        'year': year,
                        'week': week,
                        'posts': posts_list,
                        'platform': 'melon'}

            return jsonify(response)
        elif (pl == 'genie'):
            fetch_posts = music_db.week_chart_genie.aggregate([
                {"$sort": {"datetime": -1}},
                {"$match":
                     {"year":
                          {"$gt": year - 1,
                           "$lte": year}
                      }},
                {"$match": {
                    "week":
                        {"$gt": week - 1,
                         "$lte": week}
                }},
                {"$unwind": "$data"},
                {"$project": {
                    "_id": 0,
                    "year": "$ year",
                    "week": "$week",
                    "artist": "$data.artist",
                    "rank": "$data.ranking",
                    "rank_change": "$data.rank_position",
                    "title": "$data.title"
                }}
            ])
            posts_list = []
            for post in fetch_posts:
                posts_list.append(post)
            response = {'total_posts_count': posts_count_genie,
                        'year': year,
                        'week': week,
                        'posts': posts_list,
                        'platform': 'genie'}

            return jsonify(response)
        elif (pl == 'qq'):
            fetch_posts = music_db.week_chart_qq.aggregate([
                {"$sort": {"datetime": -1}},
                {"$match":
                     {"year":
                          {"$gt": year - 1,
                           "$lte": year}
                      }},
                {"$match": {
                    "week":
                        {"$gt": week - 1,
                         "$lte": week}
                }},
                {"$unwind": "$data"},
                {"$project": {
                    "_id": 0,
                    "year": "$ year",
                    "week": "$week",
                    "artist": "$data.artist",
                    "rank": "$data.ranking",
                    "rank_change": "$data.rank_position",
                    "title": "$data.title"
                }}
            ])
            posts_list = []
            for post in fetch_posts:
                posts_list.append(post)
            response = {'total_posts_count': posts_count_qq,
                        'year': year,
                        'week': week,
                        'posts': posts_list,
                        'platform': 'qq'}

            return jsonify(response)
        elif (pl == 'billboard'):
            fetch_posts = music_db.week_chart_billboard_global_two_hundred.aggregate([
                {"$sort": {"datetime": -1}},
                {"$match":
                     {"year":
                          {"$gt": year - 1,
                           "$lte": year}
                      }},
                {"$match": {
                    "week":
                        {"$gt": week - 1,
                         "$lte": week}
                }},
                {"$unwind": "$data"},
                {"$project": {
                    "_id": 0,
                    "year": "$year",
                    "week": "$week",
                    "artist": "$data.artist",
                    "rank": "$data.ranking",
                    "rank_change": "$data.rank_position",
                    "title": "$data.title",
                    "peak": "$data.peak_position",
                    "weeks on chart": "$data.weeks_on_chart"
                }}
            ])
            posts_list = []
            for post in fetch_posts:
                posts_list.append(post)
            response = {'total_posts_count': posts_count_billboard,
                        'year': year,
                        'week': week,
                        'posts': posts_list,
                        'platform': 'billboard'}

            return jsonify(response)
        elif (pl == 'youtube'):
            fetch_posts = music_db.week_chart_youtube.aggregate([
                {"$sort": {"datetime": -1}},
                {"$match":
                     {"year":
                          {"$gt": year - 1,
                           "$lte": year}
                      }},
                {"$match": {
                    "week":
                        {"$gt": week - 1,
                         "$lte": week}
                }},
                {"$unwind": "$data"},
                {"$project": {
                    "_id": 0,
                    "year": "$ year",
                    "week": "$week",
                    "artist": "$data.artist",
                    "rank": "$data.ranking",
                    "rank_position": "$data.rank_position",
                    "title": "$data.title",
                    "rank_change": "$data.rank_change",
                }}
            ])
            posts_list = []
            for post in fetch_posts:
                posts_list.append(post)
            response = {'total_posts_count': posts_count_youtube,
                        'year': year,
                        'week': week,
                        'posts': posts_list,
                        'platform': 'youtube'}

            return jsonify(response)
        else:
            fetch_posts = music_db.week_chart_spotify.aggregate([
                {"$sort": {"datetime": -1}},
                {"$match":
                     {"year":
                          {"$gt": year - 1,
                           "$lte": year}
                      }},
                {"$match": {
                    "week":
                        {"$gt": week - 1,
                         "$lte": week}
                }},
                {"$unwind": "$data"},
                {"$project": {
                    "_id": 0,
                    "year": "$year",
                    "week": "$week",
                    "artist": "$data.artist",
                    "peak": "$data.peak",
                    "rank": "$data.rank",
                    "rank_change": "$data.rank_change",
                    "streak": "$data.streak",
                    "streams": "$data.streams",
                    "title": "$data.title"
                }}
            ])
            posts_list = []
            for post in fetch_posts:
                posts_list.append(post)
            response = {'total_posts_count': posts_count_spotify,
                        'year': year,
                        'week': week,
                        'posts': posts_list,
                        'platform': 'spotify'}

            return jsonify(response)


class SpotifyTopTrackByCountry(Resource):
    def get(self):
        posts_data = reqparse.RequestParser()
        posts_data.add_argument('end', type=lambda x: datetime.datetime.strptime(x, '%Y-%m-%d'), required=True,
                                location='args')
        posts_data.add_argument('drange', type=str, required=True, location='args')
        posts_data.add_argument('country', type=str, required=True, location='args')
        data = posts_data.parse_args()
        end = data['end']
        drange = data['drange']
        country = data['country']
        _temp_list = []

        # Total number of posts of spotify
        posts_count = main_db.spotify_info.aggregate([
            {"$sort": {"datetime": -1}},
            {"$group": {
                "_id": "total",
                "count": {"$sum": {"$toInt": 1}}
            }}
        ])
        #todo

        # Case 1
        if (drange == '1d'):
            fetch_posts = main_db.spotify_info.aggregate([
                {"$sort": {"datetime": -1}},
                {"$match":
                     {"datetime":
                          {"$lte": end,
                           "$gt": end - datetime.timedelta(days=1)}
                }},
                {"$project": {
                    "_id": 0,
                    "datetime": {
                        "$dateToString": {
                            "format": "%Y-%m-%d",
                            "date": "$datetime"
                        }
                    },
                    "top_track": "$top_track"
                }},
                {"$unwind": "$top_track"},
                {"$match": {"top_track.country": country}},
                {"$project": {
                    "_id": 0,
                    "datetime": "$datetime",
                    "country": "$top_track.country",
                    "top_track": "$top_track.tracks"
                }},
            ])
            posts_list = []
            for post in fetch_posts:
                posts_list.append(post)
            response = {'country': country,
                        'range': drange,
                        'posts': posts_list}

            return jsonify(response)
        elif (drange == '3d'):
            fetch_posts = main_db.spotify_info.aggregate([
                {"$sort": {"datetime": -1}},
                {"$match":
                     {"datetime":
                          {"$lte": end,
                           "$gt": end - datetime.timedelta(days=3)}
                      }},
                {"$project": {
                    "_id": 0,
                    "datetime": {
                        "$dateToString": {
                            "format": "%Y-%m-%d",
                            "date": "$datetime"
                        }
                    },
                    "top_track": "$top_track"
                }},
                {"$unwind": "$top_track"},
                {"$match": {"top_track.country": country}},
                {"$project": {
                    "_id": 0,
                    "datetime": "$datetime",
                    "country": "$top_track.country",
                    "top_track": "$top_track.tracks"
                }}
            ])
            posts_list = []
            for post in fetch_posts:
                posts_list.append(post)
            response = {'country': country,
                        'range': drange,
                        'posts': posts_list}

            return jsonify(response)
        else:
            fetch_posts = main_db.spotify_info.aggregate([
                {"$sort": {"datetime": -1}},
                {"$limit": 1},
                {"$project": {
                    "_id": 0,
                    "datetime": {
                        "$dateToString": {
                            "format": "%Y-%m-%d",
                            "date": "$datetime"
                        }
                    },
                    "top_track": "$top_track"
                }},
                {"$unwind": "$top_track"},
                {"$match": {"top_track.country": "KR"}},
                {"$project": {
                    "_id": 0,
                    "datetime": "$datetime",
                    "country": "$top_track.country",
                    "top_track": "$top_track.tracks"
                }}
            ])
            posts_list = []
            for post in fetch_posts:
                posts_list.append(post)
            response = {'country': country,
                        'range': drange,
                        'posts': posts_list}

            return jsonify(response)


class SpotifyTopTrackPopularityByRegion(Resource):
    def get(self):
        posts_data = reqparse.RequestParser()
        posts_data.add_argument('track', type=str, required=True, location='args')
        data = posts_data.parse_args()
        track = data['track']

        select_track_list = main_db.spotify_info.aggregate([
            {"$sort": {"datetime": -1}},
            {"$limit": 1},
            {"$project": {
                "_id": 0,
                "datetime": {
                    "$dateToString": {
                        "format": "%Y-%m-%d",
                        "date": "$datetime"
                    }
                },
                "top_track": "$top_track"
            }},
            {"$unwind": "$top_track"},
            {"$project": {
                "_id": 0,
                "datetime": "$datetime",
                "region": "$top_track.region",
                "country": "$top_track.country",
                "tracks": "$top_track.tracks"
            }},
            {"$unwind": "$tracks"},
            {"$project": {
                "_id": 0,
                "datetime": "$datetime",
                "country": "$country",
                "region": "$region",
                "top_track_name": "$tracks.track",
                "top_track_popularity": "$tracks.popularity"
            }},
            {"$sort": {"top_track_popularity": -1}},
            {"$group": {
                "_id": {"region": "$region", "track": "$top_track_name"},
                "count": {"$sum": {"$toInt": 1}},
                "popularity": {"$sum": "$top_track_popularity"}
            }},
            {"$addFields": {
                "agg_popularity": {
                    "$round": [{"$divide": ["$popularity", "$count"]}, 2]}
            }},
            {"$project": {
                "_id": 0,
                "region": "$_id.region",
                "track": "$_id.track",
                "count": "$count",
                "popularity": "$popularity",
                "agg_popularity": "$agg_popularity"
            }},
            {"$group": {
                "_id": "$track",
                "region": {"$push": "$region"},
                "agg_popularity": {"$push": "$agg_popularity"}
            }},
            {"$project": {
                "track_info": {
                    "$map": {
                        "input": {"$zip": {"inputs": ["$region", "$agg_popularity"]}},
                        "in": {
                            "region": {"$arrayElemAt": ["$$this", 0]},
                            "agg_popularity": {"$arrayElemAt": ["$$this", 1]}
                        }
                    }
                }
            }},
            {"$project": {
                "_id": 0,
                "track_list": "$_id"
            }},
            {"$sort": {"track_list": 1}},
            {"$group": {
                "_id": None,
                "track": {
                    "$push": "$$ROOT.track_list"
                }
            }}
        ])

        tracks_list = []
        for post in select_track_list:
            tracks_list.append(post)

        fetch_posts = main_db.spotify_info.aggregate([
            {"$sort": {"datetime": -1}},
            {"$limit": 1},
            {"$project": {
                "_id": 0,
                "datetime": {
                    "$dateToString": {
                        "format": "%Y-%m-%d",
                        "date": "$datetime"
                    }
                },
                "top_track": "$top_track"
            }},
            {"$unwind": "$top_track"},
            {"$project": {
                "_id": 0,
                "datetime": "$datetime",
                "region": "$top_track.region",
                "country": "$top_track.country",
                "tracks": "$top_track.tracks"
            }},
            {"$unwind": "$tracks"},
            {"$project": {
                "_id": 0,
                "datetime": "$datetime",
                "country": "$country",
                "region": "$region",
                "top_track_name": "$tracks.track",
                "top_track_popularity": "$tracks.popularity"
            }},
            {"$sort": {"top_track_popularity": -1}},
            {"$group": {
                "_id": {"region": "$region", "track": "$top_track_name"},
                "count": {"$sum": {"$toInt": 1}},
                "popularity": {"$sum": "$top_track_popularity"},
                "datetime": {"$first": "$datetime"}
            }},
            {"$addFields": {
                "agg_popularity": {"$round": [{"$divide": ["$popularity", "$count"]}, 2]}
            }},
            {"$project": {
                "_id": 0,
                "region": "$_id.region",
                "track": "$_id.track",
                "count": "$count",
                "popularity": "$popularity",
                "agg_popularity": "$agg_popularity",
                "datetime": "$datetime"
            }},
            {"$group": {
                "_id": "$track",
                "region": {"$push": "$region"},
                "agg_popularity": {"$push": "$agg_popularity"},
                "datetime": {"$first": "$datetime"}
            }},
            {"$match": {
                "_id": track
            }},
            {"$project": {
                "track_info": {
                    "$map": {
                        "input": {"$zip": {"inputs": ["$region", "$agg_popularity"]}},
                        "in": {
                            "region": {"$arrayElemAt": ["$$this", 0]},
                            "agg_popularity": {"$arrayElemAt": ["$$this", 1]}
                        }
                    }
                }
            }}
        ])

        posts_list = []
        for post in fetch_posts:
            posts_list.append(post)
        response = {'track': track,
                    'track_select_list': tracks_list,
                    'result': posts_list}

        return jsonify(response)


class CircleChartRetailAlbum(Resource):
    def get(self):
        posts_data = reqparse.RequestParser()
        posts_data.add_argument('end', type=lambda x: datetime.datetime.strptime(x, '%Y-%m-%d'), required=True,
                                location='args')
        posts_data.add_argument('select', type=str, required=True, location='args')
        data = posts_data.parse_args()
        end = data['end']
        select = data['select']

        if (select == 'daily'):
            fetch_posts = general_db.daily_retail_album_gaon.aggregate([
                {"$match": {
                    "record_day":
                        {"$lte": end,
                         "$gt": end - datetime.timedelta(days=1)}
                }},
                {"$project": {
                    "_id": 0,
                    "data": "$data"
                }},
                {"$unwind": "$data"},
                {"$project": {
                    "album": "$data.album",
                    "artist": "$data.artist",
                    "domesticSum": {"$toInt": "$data.domesticSum"},
                    "abroadSum": {"$toInt": "$data.abroadSum"},
                    "total_sold": {"$toInt": "$data.total_sold_count"}
                }},
                {"$group": {
                    "_id": "$album",
                    "artist": {"$first": "$artist"},
                    "domestic": {"$sum": "$domesticSum"},
                    "abroad": {"$sum": "$abroadSum"},
                    "sum": {"$sum": "$total_sold"}
                }},
                {"$sort": {"sum": -1}}
            ])

            posts_list = []
            for post in fetch_posts:
                posts_list.append(post)
            response = {'end': end.strftime("%Y-%m-%d"),
                        'select': select,
                        'posts': posts_list}

            return jsonify(response)
        elif (select == 'weekly'):
            fetch_posts = general_db.daily_retail_album_gaon.aggregate([
                {"$match": {
                    "record_day":
                        {"$lte": end,
                         "$gt": end - datetime.timedelta(days=7)}
                }},
                {"$unwind": "$data"},
                {"$project": {
                    "album": "$data.album",
                    "artist": "$data.artist",
                    "domesticSum": {"$toInt": "$data.domesticSum"},
                    "abroadSum": {"$toInt": "$data.abroadSum"},
                    "total_sold": {"$toInt": "$data.total_sold_count"}
                }},
                {"$group": {
                    "_id": "$album",
                    "artist": {"$first": "$artist"},
                    "domestic": {"$sum": "$domesticSum"},
                    "abroad": {"$sum": "$abroadSum"},
                    "sum": {"$sum": "$total_sold"}
                }},
                {"$sort": {"sum": -1}}
            ])

            posts_list = []
            for post in fetch_posts:
                posts_list.append(post)
            response = {'end': end.strftime("%Y-%m-%d"),
                        'select': select,
                        'posts': posts_list}

            return jsonify(response)
        elif (select == 'monthly'):
            fetch_posts = general_db.daily_retail_album_gaon.aggregate([
                {"$match": {
                    "record_day":
                        {"$lte": end,
                         "$gt": end - datetime.timedelta(days=30)}
                }},
                {"$unwind": "$data"},
                {"$project": {
                    "album": "$data.album",
                    "artist": "$data.artist",
                    "domesticSum": {"$toInt": "$data.domesticSum"},
                    "abroadSum": {"$toInt": "$data.abroadSum"},
                    "total_sold": {"$toInt": "$data.total_sold_count"}
                }},
                {"$group": {
                    "_id": "$album",
                    "artist": {"$first": "$artist"},
                    "domestic": {"$sum": "$domesticSum"},
                    "abroad": {"$sum": "$abroadSum"},
                    "sum": {"$sum": "$total_sold"}
                }},
                {"$sort": {"sum": -1}}
            ])

            posts_list = []
            for post in fetch_posts:
                posts_list.append(post)
            response = {'end': end.strftime("%Y-%m-%d"),
                        'select': select,
                        'posts': posts_list}

            return jsonify(response)
        elif (select == 'yearly'):
            fetch_posts = general_db.daily_retail_album_gaon.aggregate([
                {"$match": {
                    "record_day":
                        {"$lte": end,
                         "$gt": end - datetime.timedelta(days=365)}
                }},
                {"$unwind": "$data"},
                {"$project": {
                    "album": "$data.album",
                    "artist": "$data.artist",
                    "domesticSum": {"$toInt": "$data.domesticSum"},
                    "abroadSum": {"$toInt": "$data.abroadSum"},
                    "total_sold": {"$toInt": "$data.total_sold_count"}
                }},
                {"$group": {
                    "_id": "$album",
                    "artist": {"$first": "$artist"},
                    "domestic": {"$sum": "$domesticSum"},
                    "abroad": {"$sum": "$abroadSum"},
                    "sum": {"$sum": "$total_sold"}
                }},
                {"$sort": {"sum": -1}}
            ])

            posts_list = []
            for post in fetch_posts:
                posts_list.append(post)
            response = {'end': end.strftime("%Y-%m-%d"),
                        'select': select,
                        'posts': posts_list}

            return jsonify(response)
        else:
            fetch_posts = general_db.daily_retail_album_gaon.aggregate([
                {"$match": {
                    "record_day":
                        {"$lte": end,
                         "$gt": end - datetime.timedelta(days=1)}
                }},
                {"$unwind": "$data"},
                {"$project": {
                    "album": "$data.album",
                    "artist": "$data.artist",
                    "domesticSum": {"$toInt": "$data.domesticSum"},
                    "abroadSum": {"$toInt": "$data.abroadSum"},
                    "total_sold": {"$toInt": "$data.total_sold_count"}
                }},
                {"$group": {
                    "_id": "$album",
                    "artist": {"$first": "$artist"},
                    "domestic": {"$sum": "$domesticSum"},
                    "abroad": {"$sum": "$abroadSum"},
                    "sum": {"$sum": "$total_sold"}
                }},
                {"$sort": {"sum": -1}}
            ])

            posts_list = []
            for post in fetch_posts:
                posts_list.append(post)
            response = {'end': end.strftime("%Y-%m-%d"),
                        'select': select,
                        'posts': posts_list}

            return jsonify(response)
