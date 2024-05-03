from models import main_db, yt_db
from flask import jsonify, Blueprint
from bson.json_util import dumps
import datetime
from datetime import timedelta
from flask_restful import Resource, reqparse, Api
import pandas as pd
from collections import Counter
import numpy as np


youtube_api_bp = Blueprint('youtube_api', __name__)
youtube_api = Api(youtube_api_bp)

# extract keywords with hashtag from string
def extract_hashtags_keyword(text):
    # initializing hashtag_list variable
    hashtag_list = []

    # splitting the text into words
    for word in text.split():
        # checking the first character of every word
        if word[0] == '#':
            # adding the word to the hashtag_list
            hashtag_list.append(word[1:])
    return hashtag_list

@youtube_api_bp.route('/youtube/stats/video', methods=['GET'])
def get_youtube_daily_count():
    try:
        results = main_db.youtube_video_info.aggregate([
            {"$sort": {"datetime": -1}},
            {"$unwind": "$video_data"},
            {"$project": {
                "_id": 0,
                "datetime": "$datetime",
                "published_at": "$video_data.publishedAt",
                "view_count": {"$toInt": "$video_data.viewCount"},
                "like_count": {"$toInt": "$video_data.likeCount"},
                "favorite_count": {"$toInt": "$video_data.favoriteCount"},
                "comment_count": {"$toInt": "$video_data.commentCount"}
            }},
            {"$group": {
                "_id": "$datetime",
                "video_num": {"$sum": {"$toInt": 1}},
                "total_view": {"$sum": "$view_count"},
                "total_like": {"$sum": "$like_count"},
                "total_favorite": {"$sum": "$favorite_count"},
                "total_comment": {"$sum": "$comment_count"}
            }},
            {"$sort": {"_id": 1}},
            {"$addFields": {
                "sub_total": {
                    "$sum": ["$total_like", "$total_comment", "$total_favorite"]}
            }},
            {"$project": {
                "datetime": "$_id",
                "video_num": "$video_num",
                "eng_rate": {
                    "$round": [
                        {"$multiply": [{"$divide": ["$sub_total", "$total_view"]}, 100]}, 2
                    ]
                },
                "total_view": "$total_view",
                "total_like": "$total_like",
                "total_comment": "$total_comment",
                "total_favorite": "$total_favorite",
                "avg_like": {
                    "$round": [{"$divide": ["$total_like", "$video_num"]}, 2]
                },
                "avg_comment": {
                    "$round": [{"$divide": ["$total_comment", "$video_num"]}, 2]
                },
                "avg_favorite": {
                    "$round": [{"$divide": ["$total_favorite", "$video_num"]}, 2]
                }
            }}
        ])
        _blank = []
        for item in results:
            _blank.append(item)
        # convert list to df, then fill nan with 0
        _view = [ele["total_view"] for ele in _blank]
        _date = [ele["_id"] for ele in _blank]
        _eng_rate = [ele["eng_rate"] for ele in _blank]
        _like = [ele["total_like"] for ele in _blank]
        _video_num = [ele["video_num"] for ele in _blank]
        _comment = [ele["total_comment"] for ele in _blank]
        _favorite = [ele["total_favorite"] for ele in _blank]
        _avg_like = [ele["avg_like"] for ele in _blank]
        _avg_comment = [ele["avg_comment"] for ele in _blank]
        _avg_favorite = [ele["avg_favorite"] for ele in _blank]

        df = pd.DataFrame(list(zip(_date, _video_num, _view, _like, _comment, _favorite,
                                   _avg_like, _avg_comment, _avg_favorite)),
                          columns=['datetime', 'video_num', 'total_view', 'total_like', 'total_comment',
                                   'total_favorite', 'avg_like', 'avg_comment', 'avg_favorite'])
        df = df.fillna(0)
        df["datetime"] = pd.to_datetime(df["datetime"])
        df["datetime"] = df["datetime"].dt.strftime("%Y-%m-%d")
        result = df.to_dict(orient='records')

        return dumps({'result': result})
    except Exception as e:
        return dumps({'error': str(e)})

@youtube_api_bp.route('/youtube/stats/channel', methods=['GET'])
def get_youtube_channel_index():
    try:
        results = main_db.youtube_index.aggregate([
            {"$sort": {"datetime": -1}},
            {"$project": {
                "datetime": {
                    "$dateToString": {
                        "format": "%Y-%m-%d",
                        "date": {
                            "$dateFromString": {
                                "dateString": "$datetime"
                            }}
                    }},
                "_id": 0,
                "subscriber": {"$toInt": "$data.subscriberCount"},
                "total_view": {"$toInt": "$data.viewCount"},
                "video_num":  {"$toInt": "$data.videoCount"}
            }},
            {"$sort": {"datetime": 1}}
        ])
        _blank_list = []
        for item in results:
            _blank_list.append(item)

        _view = [ele["total_view"] for ele in _blank_list]
        _date = [ele["datetime"] for ele in _blank_list]
        _subscriber = [ele["subscriber"] for ele in _blank_list]
        _video_num = [ele["video_num"] for ele in _blank_list]
        # calculate difference
        _view_diff = [y-x for x, y in zip(_view, _view[1:-2])]
        _date_diff = _date[1:-2]
        # convert list to df then dict
        df = pd.DataFrame(list(zip(_date_diff, _subscriber, _video_num, _view, _view_diff)),
                          columns=['datetime', 'subscriber', 'video_num', 'total_channel_view', 'channel_view_difference'])
        result = df.to_dict(orient='records')

        return dumps({'result': result})
    except Exception as e:
        return dumps({'err': str(e)})

@youtube_api_bp.route('/youtube/stats/country', methods=['GET'])
def get_youtube_country():
    '''
    calculate user language percentage
    :return:
    '''
    try:
        results = main_db.youtube_comment.aggregate([
            {"$group": {
                "_id": "$author_channel_id",
                "country": {"$first": "$country"}
            }},
            {"$match": {"country": {"$ne": None}}},
            {"$group": {
                "_id": "null",
                "country": {"$push": "$country"},
                "total": {"$sum": {"$toInt": 1}},
            }},
            {"$unwind": "$country"},
            {"$group": {
                "_id": "$country",
                "count": {"$sum": {"$toInt": 1}},
                "total": {"$first": "$total"}
            }},
            {"$project": {
                "_id": 0,
                "code": "$_id",
                "percentage": {
                    "$round": [{"$multiply": [{"$divide": ["$count", "$total"]}, 100]}, 2]
                }
            }},
            {"$sort": {"percentage": -1}},
            {"$limit": 10}
        ])

        blank_list = []
        for item in results:
            blank_list.append(item)
        country_abbr = [
            {
                "code": "AF",
                "Name": "Afghanistan"
            },
            {
                "code": "AX",
                "Name": "Åland Islands"
            },
            {
                "code": "AL",
                "Name": "Albania"
            },
            {
                "code": "DZ",
                "Name": "Algeria"
            },
            {
                "code": "AS",
                "Name": "American Samoa"
            },
            {
                "code": "AD",
                "Name": "Andorra"
            },
            {
                "code": "AO",
                "Name": "Angola"
            },
            {
                "code": "AI",
                "Name": "Anguilla"
            },
            {
                "code": "AQ",
                "Name": "Antarctica"
            },
            {
                "code": "AG",
                "Name": "Antigua and Barbuda"
            },
            {
                "code": "AR",
                "Name": "Argentina"
            },
            {
                "code": "AM",
                "Name": "Armenia"
            },
            {
                "code": "AW",
                "Name": "Aruba"
            },
            {
                "code": "AU",
                "Name": "Australia"
            },
            {
                "code": "AT",
                "Name": "Austria"
            },
            {
                "code": "AZ",
                "Name": "Azerbaijan"
            },
            {
                "code": "BS",
                "Name": "Bahamas"
            },
            {
                "code": "BH",
                "Name": "Bahrain"
            },
            {
                "code": "BD",
                "Name": "Bangladesh"
            },
            {
                "code": "BB",
                "Name": "Barbados"
            },
            {
                "code": "BY",
                "Name": "Belarus"
            },
            {
                "code": "BE",
                "Name": "Belgium"
            },
            {
                "code": "BZ",
                "Name": "Belize"
            },
            {
                "code": "BJ",
                "Name": "Benin"
            },
            {
                "code": "BM",
                "Name": "Bermuda"
            },
            {
                "code": "BT",
                "Name": "Bhutan"
            },
            {
                "code": "BO",
                "Name": "Bolivia, Plurinational State of"
            },
            {
                "code": "BQ",
                "Name": "Bonaire, Sint Eustatius and Saba"
            },
            {
                "code": "BA",
                "Name": "Bosnia and Herzegovina"
            },
            {
                "code": "BW",
                "Name": "Botswana"
            },
            {
                "code": "BV",
                "Name": "Bouvet Island"
            },
            {
                "code": "BR",
                "Name": "Brazil"
            },
            {
                "code": "IO",
                "Name": "British Indian Ocean Territory"
            },
            {
                "code": "BN",
                "Name": "Brunei Darussalam"
            },
            {
                "code": "BG",
                "Name": "Bulgaria"
            },
            {
                "code": "BF",
                "Name": "Burkina Faso"
            },
            {
                "code": "BI",
                "Name": "Burundi"
            },
            {
                "code": "KH",
                "Name": "Cambodia"
            },
            {
                "code": "CM",
                "Name": "Cameroon"
            },
            {
                "code": "CA",
                "Name": "Canada"
            },
            {
                "code": "CV",
                "Name": "Cape Verde"
            },
            {
                "code": "KY",
                "Name": "Cayman Islands"
            },
            {
                "code": "CF",
                "Name": "Central African Republic"
            },
            {
                "code": "TD",
                "Name": "Chad"
            },
            {
                "code": "CL",
                "Name": "Chile"
            },
            {
                "code": "CN",
                "Name": "China"
            },
            {
                "code": "CX",
                "Name": "Christmas Island"
            },
            {
                "code": "CC",
                "Name": "Cocos (Keeling) Islands"
            },
            {
                "code": "CO",
                "Name": "Colombia"
            },
            {
                "code": "KM",
                "Name": "Comoros"
            },
            {
                "code": "CG",
                "Name": "Congo"
            },
            {
                "code": "CD",
                "Name": "Congo, the Democratic Republic of the"
            },
            {
                "code": "CK",
                "Name": "Cook Islands"
            },
            {
                "code": "CR",
                "Name": "Costa Rica"
            },
            {
                "code": "CI",
                "Name": "Côte d'Ivoire"
            },
            {
                "code": "HR",
                "Name": "Croatia"
            },
            {
                "code": "CU",
                "Name": "Cuba"
            },
            {
                "code": "CW",
                "Name": "Curaçao"
            },
            {
                "code": "CY",
                "Name": "Cyprus"
            },
            {
                "code": "CZ",
                "Name": "Czech Republic"
            },
            {
                "code": "DK",
                "Name": "Denmark"
            },
            {
                "code": "DJ",
                "Name": "Djibouti"
            },
            {
                "code": "DM",
                "Name": "Dominica"
            },
            {
                "code": "DO",
                "Name": "Dominican Republic"
            },
            {
                "code": "EC",
                "Name": "Ecuador"
            },
            {
                "code": "EG",
                "Name": "Egypt"
            },
            {
                "code": "SV",
                "Name": "El Salvador"
            },
            {
                "code": "GQ",
                "Name": "Equatorial Guinea"
            },
            {
                "code": "ER",
                "Name": "Eritrea"
            },
            {
                "code": "EE",
                "Name": "Estonia"
            },
            {
                "code": "ET",
                "Name": "Ethiopia"
            },
            {
                "code": "FK",
                "Name": "Falkland Islands (Malvinas)"
            },
            {
                "code": "FO",
                "Name": "Faroe Islands"
            },
            {
                "code": "FJ",
                "Name": "Fiji"
            },
            {
                "code": "FI",
                "Name": "Finland"
            },
            {
                "code": "FR",
                "Name": "France"
            },
            {
                "code": "GF",
                "Name": "French Guiana"
            },
            {
                "code": "PF",
                "Name": "French Polynesia"
            },
            {
                "code": "TF",
                "Name": "French Southern Territories"
            },
            {
                "code": "GA",
                "Name": "Gabon"
            },
            {
                "code": "GM",
                "Name": "Gambia"
            },
            {
                "code": "GE",
                "Name": "Georgia"
            },
            {
                "code": "DE",
                "Name": "Germany"
            },
            {
                "code": "GH",
                "Name": "Ghana"
            },
            {
                "code": "GI",
                "Name": "Gibraltar"
            },
            {
                "code": "GR",
                "Name": "Greece"
            },
            {
                "code": "GL",
                "Name": "Greenland"
            },
            {
                "code": "GD",
                "Name": "Grenada"
            },
            {
                "code": "GP",
                "Name": "Guadeloupe"
            },
            {
                "code": "GU",
                "Name": "Guam"
            },
            {
                "code": "GT",
                "Name": "Guatemala"
            },
            {
                "code": "GG",
                "Name": "Guernsey"
            },
            {
                "code": "GN",
                "Name": "Guinea"
            },
            {
                "code": "GW",
                "Name": "Guinea-Bissau"
            },
            {
                "code": "GY",
                "Name": "Guyana"
            },
            {
                "code": "HT",
                "Name": "Haiti"
            },
            {
                "code": "HM",
                "Name": "Heard Island and McDonald Islands"
            },
            {
                "code": "VA",
                "Name": "Holy See (Vatican City State)"
            },
            {
                "code": "HN",
                "Name": "Honduras"
            },
            {
                "code": "HK",
                "Name": "Hong Kong"
            },
            {
                "code": "HU",
                "Name": "Hungary"
            },
            {
                "code": "IS",
                "Name": "Iceland"
            },
            {
                "code": "IN",
                "Name": "India"
            },
            {
                "code": "ID",
                "Name": "Indonesia"
            },
            {
                "code": "IR",
                "Name": "Iran, Islamic Republic of"
            },
            {
                "code": "IQ",
                "Name": "Iraq"
            },
            {
                "code": "IE",
                "Name": "Ireland"
            },
            {
                "code": "IM",
                "Name": "Isle of Man"
            },
            {
                "code": "IL",
                "Name": "Israel"
            },
            {
                "code": "IT",
                "Name": "Italy"
            },
            {
                "code": "JM",
                "Name": "Jamaica"
            },
            {
                "code": "JP",
                "Name": "Japan"
            },
            {
                "code": "JE",
                "Name": "Jersey"
            },
            {
                "code": "JO",
                "Name": "Jordan"
            },
            {
                "code": "KZ",
                "Name": "Kazakhstan"
            },
            {
                "code": "KE",
                "Name": "Kenya"
            },
            {
                "code": "KI",
                "Name": "Kiribati"
            },
            {
                "code": "KP",
                "Name": "Korea, Democratic People's Republic of"
            },
            {
                "code": "KR",
                "Name": "Korea, Republic of"
            },
            {
                "code": "KW",
                "Name": "Kuwait"
            },
            {
                "code": "KG",
                "Name": "Kyrgyzstan"
            },
            {
                "code": "LA",
                "Name": "Lao People's Democratic Republic"
            },
            {
                "code": "LV",
                "Name": "Latvia"
            },
            {
                "code": "LB",
                "Name": "Lebanon"
            },
            {
                "code": "LS",
                "Name": "Lesotho"
            },
            {
                "code": "LR",
                "Name": "Liberia"
            },
            {
                "code": "LY",
                "Name": "Libya"
            },
            {
                "code": "LI",
                "Name": "Liechtenstein"
            },
            {
                "code": "LT",
                "Name": "Lithuania"
            },
            {
                "code": "LU",
                "Name": "Luxembourg"
            },
            {
                "code": "MO",
                "Name": "Macao"
            },
            {
                "code": "MK",
                "Name": "Macedonia, the Former Yugoslav Republic of"
            },
            {
                "code": "MG",
                "Name": "Madagascar"
            },
            {
                "code": "MW",
                "Name": "Malawi"
            },
            {
                "code": "MY",
                "Name": "Malaysia"
            },
            {
                "code": "MV",
                "Name": "Maldives"
            },
            {
                "code": "ML",
                "Name": "Mali"
            },
            {
                "code": "MT",
                "Name": "Malta"
            },
            {
                "code": "MH",
                "Name": "Marshall Islands"
            },
            {
                "code": "MQ",
                "Name": "Martinique"
            },
            {
                "code": "MR",
                "Name": "Mauritania"
            },
            {
                "code": "MU",
                "Name": "Mauritius"
            },
            {
                "code": "YT",
                "Name": "Mayotte"
            },
            {
                "code": "MX",
                "Name": "Mexico"
            },
            {
                "code": "FM",
                "Name": "Micronesia, Federated States of"
            },
            {
                "code": "MD",
                "Name": "Moldova, Republic of"
            },
            {
                "code": "MC",
                "Name": "Monaco"
            },
            {
                "code": "MN",
                "Name": "Mongolia"
            },
            {
                "code": "ME",
                "Name": "Montenegro"
            },
            {
                "code": "MS",
                "Name": "Montserrat"
            },
            {
                "code": "MA",
                "Name": "Morocco"
            },
            {
                "code": "MZ",
                "Name": "Mozambique"
            },
            {
                "code": "MM",
                "Name": "Myanmar"
            },
            {
                "code": "NA",
                "Name": "Namibia"
            },
            {
                "code": "NR",
                "Name": "Nauru"
            },
            {
                "code": "NP",
                "Name": "Nepal"
            },
            {
                "code": "NL",
                "Name": "Netherlands"
            },
            {
                "code": "NC",
                "Name": "New Caledonia"
            },
            {
                "code": "NZ",
                "Name": "New Zealand"
            },
            {
                "code": "NI",
                "Name": "Nicaragua"
            },
            {
                "code": "NE",
                "Name": "Niger"
            },
            {
                "code": "NG",
                "Name": "Nigeria"
            },
            {
                "code": "NU",
                "Name": "Niue"
            },
            {
                "code": "NF",
                "Name": "Norfolk Island"
            },
            {
                "code": "MP",
                "Name": "Northern Mariana Islands"
            },
            {
                "code": "NO",
                "Name": "Norway"
            },
            {
                "code": "OM",
                "Name": "Oman"
            },
            {
                "code": "PK",
                "Name": "Pakistan"
            },
            {
                "code": "PW",
                "Name": "Palau"
            },
            {
                "code": "PS",
                "Name": "Palestine, State of"
            },
            {
                "code": "PA",
                "Name": "Panama"
            },
            {
                "code": "PG",
                "Name": "Papua New Guinea"
            },
            {
                "code": "PY",
                "Name": "Paraguay"
            },
            {
                "code": "PE",
                "Name": "Peru"
            },
            {
                "code": "PH",
                "Name": "Philippines"
            },
            {
                "code": "PN",
                "Name": "Pitcairn"
            },
            {
                "code": "PL",
                "Name": "Poland"
            },
            {
                "code": "PT",
                "Name": "Portugal"
            },
            {
                "code": "PR",
                "Name": "Puerto Rico"
            },
            {
                "code": "QA",
                "Name": "Qatar"
            },
            {
                "code": "RE",
                "Name": "Réunion"
            },
            {
                "code": "RO",
                "Name": "Romania"
            },
            {
                "code": "RU",
                "Name": "Russian Federation"
            },
            {
                "code": "RW",
                "Name": "Rwanda"
            },
            {
                "code": "BL",
                "Name": "Saint Barthélemy"
            },
            {
                "code": "SH",
                "Name": "Saint Helena, Ascension and Tristan da Cunha"
            },
            {
                "code": "KN",
                "Name": "Saint Kitts and Nevis"
            },
            {
                "code": "LC",
                "Name": "Saint Lucia"
            },
            {
                "code": "MF",
                "Name": "Saint Martin (French part)"
            },
            {
                "code": "PM",
                "Name": "Saint Pierre and Miquelon"
            },
            {
                "code": "VC",
                "Name": "Saint Vincent and the Grenadines"
            },
            {
                "code": "WS",
                "Name": "Samoa"
            },
            {
                "code": "SM",
                "Name": "San Marino"
            },
            {
                "code": "ST",
                "Name": "Sao Tome and Principe"
            },
            {
                "code": "SA",
                "Name": "Saudi Arabia"
            },
            {
                "code": "SN",
                "Name": "Senegal"
            },
            {
                "code": "RS",
                "Name": "Serbia"
            },
            {
                "code": "SC",
                "Name": "Seychelles"
            },
            {
                "code": "SL",
                "Name": "Sierra Leone"
            },
            {
                "code": "SG",
                "Name": "Singapore"
            },
            {
                "code": "SX",
                "Name": "Sint Maarten (Dutch part)"
            },
            {
                "code": "SK",
                "Name": "Slovakia"
            },
            {
                "code": "SI",
                "Name": "Slovenia"
            },
            {
                "code": "SB",
                "Name": "Solomon Islands"
            },
            {
                "code": "SO",
                "Name": "Somalia"
            },
            {
                "code": "ZA",
                "Name": "South Africa"
            },
            {
                "code": "GS",
                "Name": "South Georgia and the South Sandwich Islands"
            },
            {
                "code": "SS",
                "Name": "South Sudan"
            },
            {
                "code": "ES",
                "Name": "Spain"
            },
            {
                "code": "LK",
                "Name": "Sri Lanka"
            },
            {
                "code": "SD",
                "Name": "Sudan"
            },
            {
                "code": "SR",
                "Name": "Suriname"
            },
            {
                "code": "SJ",
                "Name": "Svalbard and Jan Mayen"
            },
            {
                "code": "SZ",
                "Name": "Swaziland"
            },
            {
                "code": "SE",
                "Name": "Sweden"
            },
            {
                "code": "CH",
                "Name": "Switzerland"
            },
            {
                "code": "SY",
                "Name": "Syrian Arab Republic"
            },
            {
                "code": "TW",
                "Name": "Taiwan, Province of China"
            },
            {
                "code": "TJ",
                "Name": "Tajikistan"
            },
            {
                "code": "TZ",
                "Name": "Tanzania, United Republic of"
            },
            {
                "code": "TH",
                "Name": "Thailand"
            },
            {
                "code": "TL",
                "Name": "Timor-Leste"
            },
            {
                "code": "TG",
                "Name": "Togo"
            },
            {
                "code": "TK",
                "Name": "Tokelau"
            },
            {
                "code": "TO",
                "Name": "Tonga"
            },
            {
                "code": "TT",
                "Name": "Trinidad and Tobago"
            },
            {
                "code": "TN",
                "Name": "Tunisia"
            },
            {
                "code": "TR",
                "Name": "Turkey"
            },
            {
                "code": "TM",
                "Name": "Turkmenistan"
            },
            {
                "code": "TC",
                "Name": "Turks and Caicos Islands"
            },
            {
                "code": "TV",
                "Name": "Tuvalu"
            },
            {
                "code": "UG",
                "Name": "Uganda"
            },
            {
                "code": "UA",
                "Name": "Ukraine"
            },
            {
                "code": "AE",
                "Name": "United Arab Emirates"
            },
            {
                "code": "GB",
                "Name": "United Kingdom"
            },
            {
                "code": "US",
                "Name": "United States"
            },
            {
                "code": "UM",
                "Name": "United States Minor Outlying Islands"
            },
            {
                "code": "UY",
                "Name": "Uruguay"
            },
            {
                "code": "UZ",
                "Name": "Uzbekistan"
            },
            {
                "code": "VU",
                "Name": "Vanuatu"
            },
            {
                "code": "VE",
                "Name": "Venezuela, Bolivarian Republic of"
            },
            {
                "code": "VN",
                "Name": "Viet Nam"
            },
            {
                "code": "VG",
                "Name": "Virgin Islands, British"
            },
            {
                "code": "VI",
                "Name": "Virgin Islands, U.S."
            },
            {
                "code": "WF",
                "Name": "Wallis and Futuna"
            },
            {
                "code": "EH",
                "Name": "Western Sahara"
            },
            {
                "code": "YE",
                "Name": "Yemen"
            },
            {
                "code": "ZM",
                "Name": "Zambia"
            },
            {
                "code": "ZW",
                "Name": "Zimbabwe"
            }
        ]

        result_df = pd.DataFrame(blank_list)
        abbr_df = pd.DataFrame(country_abbr)

        df_out = result_df.merge(abbr_df, on='code')
        final_result = df_out.to_dict(orient='records')
        return dumps({'result': final_result})
    except Exception as e:
        return dumps({'err': str(e)})

@youtube_api_bp.route('/youtube/stats/language', methods=['GET'])
def get_youtube_language():
    try:
        result = main_db.youtube_comment.aggregate([
            {"$group": {
                "_id": "$author_channel_id",
                "language": {"$first": "$language"}
            }},
            {"$match": {"language": {"$ne": "UNKNOWN"}}},
            {"$group": {
                "_id": None,
                "language": {"$push": "$language"},
                "total": {"$sum": {"$toInt": 1}}
            }},
            {"$unwind": "$language"},
            {"$group": {
                "_id": "$language",
                "count": {"$sum": {"$toInt": 1}},
                "total": {"$first": "$total"}
            }},
            {"$project": {
                "_id": 0,
                "language": "$_id",
                "percentage": {
                    "$round": [{"$multiply": [{"$divide": ["$count", "$total"]}, 100]}, 2]
                }
            }},
            {"$sort": {"percentage": -1}},
            {"$limit": 6}
        ])
        blank_list = []
        for item in result:
            blank_list.append(item)

        language_abbr = [
            {"language": "aa", "name": "Afar"},
            {"language": "ab", "name": "Abkhazian"},
            {"language": "ae", "name": "Avestan"},
            {"language": "af", "name": "Afrikaans"},
            {"language": "ak", "name": "Akan"},
            {"language": "am", "name": "Amharic"},
            {"language": "an", "name": "Aragonese"},
            {"language": "ar", "name": "Arabic"},
            {"language": "as", "name": "Assamese"},
            {"language": "av", "name": "Avaric"},
            {"language": "ay", "name": "Aymara"},
            {"language": "az", "name": "Azerbaijani"},
            {"language": "ba", "name": "Bashkir"},
            {"language": "be", "name": "Belarusian"},
            {"language": "bg", "name": "Bulgarian"},
            {"language": "bh", "name": "Bihari languages"},
            {"language": "bi", "name": "Bislama"},
            {"language": "bm", "name": "Bambara"},
            {"language": "bn", "name": "Bengali"},
            {"language": "bo", "name": "Tibetan"},
            {"language": "br", "name": "Breton"},
            {"language": "bs", "name": "Bosnian"},
            {"language": "ca", "name": "Catalan; Valencian"},
            {"language": "ce", "name": "Chechen"},
            {"language": "ch", "name": "Chamorro"},
            {"language": "co", "name": "Corsican"},
            {"language": "cr", "name": "Cree"},
            {"language": "cs", "name": "Czech"},
            {
                "language": "cu",
                "name": "Church Slavic; Old Slavonic; Church Slavonic; Old Bulgarian; Old Church Slavonic"
            },
            {"language": "cv", "name": "Chuvash"},
            {"language": "cy", "name": "Welsh"},
            {"language": "da", "name": "Danish"},
            {"language": "de", "name": "German"},
            {"language": "dv", "name": "Divehi; Dhivehi; Maldivian"},
            {"language": "dz", "name": "Dzongkha"},
            {"language": "ee", "name": "Ewe"},
            {"language": "el", "name": "Greek, Modern (1453-)"},
            {"language": "en", "name": "English"},
            {"language": "eo", "name": "Esperanto"},
            {"language": "es", "name": "Spanish; Castilian"},
            {"language": "et", "name": "Estonian"},
            {"language": "eu", "name": "Basque"},
            {"language": "fa", "name": "Persian"},
            {"language": "ff", "name": "Fulah"},
            {"language": "fi", "name": "Finnish"},
            {"language": "fj", "name": "Fijian"},
            {"language": "fo", "name": "Faroese"},
            {"language": "fr", "name": "French"},
            {"language": "fy", "name": "Western Frisian"},
            {"language": "ga", "name": "Irish"},
            {"language": "gd", "name": "Gaelic; Scomttish Gaelic"},
            {"language": "gl", "name": "Galician"},
            {"language": "gn", "name": "Guarani"},
            {"language": "gu", "name": "Gujarati"},
            {"language": "gv", "name": "Manx"},
            {"language": "ha", "name": "Hausa"},
            {"language": "he", "name": "Hebrew"},
            {"language": "hi", "name": "Hindi"},
            {"language": "ho", "name": "Hiri Motu"},
            {"language": "hr", "name": "Croatian"},
            {"language": "ht", "name": "Haitian; Haitian Creole"},
            {"language": "hu", "name": "Hungarian"},
            {"language": "hy", "name": "Armenian"},
            {"language": "hz", "name": "Herero"},
            {
                "language": "ia",
                "name": "Interlingua (International Auxiliary Language Association)"
            },
            {"language": "id", "name": "Indonesian"},
            {"language": "ie", "name": "Interlingue; Occidental"},
            {"language": "ig", "name": "Igbo"},
            {"language": "ii", "name": "Sichuan Yi; Nuosu"},
            {"language": "ik", "name": "Inupiaq"},
            {"language": "io", "name": "Ido"},
            {"language": "is", "name": "Icelandic"},
            {"language": "it", "name": "Italian"},
            {"language": "iu", "name": "Inuktitut"},
            {"language": "ja", "name": "Japanese"},
            {"language": "jv", "name": "Javanese"},
            {"language": "ka", "name": "Georgian"},
            {"language": "kg", "name": "Kongo"},
            {"language": "ki", "name": "Kikuyu; Gikuyu"},
            {"language": "kj", "name": "Kuanyama; Kwanyama"},
            {"language": "kk", "name": "Kazakh"},
            {"language": "kl", "name": "Kalaallisut; Greenlandic"},
            {"language": "km", "name": "Central Khmer"},
            {"language": "kn", "name": "Kannada"},
            {"language": "ko", "name": "Korean"},
            {"language": "kr", "name": "Kanuri"},
            {"language": "ks", "name": "Kashmiri"},
            {"language": "ku", "name": "Kurdish"},
            {"language": "kv", "name": "Komi"},
            {"language": "kw", "name": "Cornish"},
            {"language": "ky", "name": "Kirghiz; Kyrgyz"},
            {"language": "la", "name": "Latin"},
            {"language": "lb", "name": "Luxembourgish; Letzeburgesch"},
            {"language": "lg", "name": "Ganda"},
            {"language": "li", "name": "Limburgan; Limburger; Limburgish"},
            {"language": "ln", "name": "Lingala"},
            {"language": "lo", "name": "Lao"},
            {"language": "lt", "name": "Lithuanian"},
            {"language": "lu", "name": "Luba-Katanga"},
            {"language": "lv", "name": "Latvian"},
            {"language": "mg", "name": "Malagasy"},
            {"language": "mh", "name": "Marshallese"},
            {"language": "mi", "name": "Maori"},
            {"language": "mk", "name": "Macedonian"},
            {"language": "ml", "name": "Malayalam"},
            {"language": "mn", "name": "Mongolian"},
            {"language": "mr", "name": "Marathi"},
            {"language": "ms", "name": "Malay"},
            {"language": "mt", "name": "Maltese"},
            {"language": "my", "name": "Burmese"},
            {"language": "na", "name": "Nauru"},
            {
                "language": "nb",
                "name": "Bokmål, Norwegian; Norwegian Bokmål"
            },
            {"language": "nd", "name": "Ndebele, North; North Ndebele"},
            {"language": "ne", "name": "Nepali"},
            {"language": "ng", "name": "Ndonga"},
            {"language": "nl", "name": "Dutch; Flemish"},
            {"language": "nn", "name": "Norwegian Nynorsk; Nynorsk, Norwegian"},
            {"language": "no", "name": "Norwegian"},
            {"language": "nr", "name": "Ndebele, South; South Ndebele"},
            {"language": "nv", "name": "Navajo; Navaho"},
            {"language": "ny", "name": "Chichewa; Chewa; Nyanja"},
            {"language": "oc", "name": "Occitan (post 1500)"},
            {"language": "oj", "name": "Ojibwa"},
            {"language": "om", "name": "Oromo"},
            {"language": "or", "name": "Oriya"},
            {"language": "os", "name": "Ossetian; Ossetic"},
            {"language": "pa", "name": "Panjabi; Punjabi"},
            {"language": "pi", "name": "Pali"},
            {"language": "pl", "name": "Polish"},
            {"language": "ps", "name": "Pushto; Pashto"},
            {"language": "pt", "name": "Portuguese"},
            {"language": "qu", "name": "Quechua"},
            {"language": "rm", "name": "Romansh"},
            {"language": "rn", "name": "Rundi"},
            {"language": "ro", "name": "Romanian; Moldavian; Moldovan"},
            {"language": "ru", "name": "Russian"},
            {"language": "rw", "name": "Kinyarwanda"},
            {"language": "sa", "name": "Sanskrit"},
            {"language": "sc", "name": "Sardinian"},
            {"language": "sd", "name": "Sindhi"},
            {"language": "se", "name": "Northern Sami"},
            {"language": "sg", "name": "Sango"},
            {"language": "si", "name": "Sinhala; Sinhalese"},
            {"language": "sk", "name": "Slovak"},
            {"language": "sl", "name": "Slovenian"},
            {"language": "sm", "name": "Samoan"},
            {"language": "sn", "name": "Shona"},
            {"language": "so", "name": "Somali"},
            {"language": "sq", "name": "Albanian"},
            {"language": "sr", "name": "Serbian"},
            {"language": "ss", "name": "Swati"},
            {"language": "st", "name": "Sotho, Southern"},
            {"language": "su", "name": "Sundanese"},
            {"language": "sv", "name": "Swedish"},
            {"language": "sw", "name": "Swahili"},
            {"language": "ta", "name": "Tamil"},
            {"language": "te", "name": "Telugu"},
            {"language": "tg", "name": "Tajik"},
            {"language": "th", "name": "Thai"},
            {"language": "ti", "name": "Tigrinya"},
            {"language": "tk", "name": "Turkmen"},
            {"language": "tl", "name": "Tagalog"},
            {"language": "tn", "name": "Tswana"},
            {"language": "to", "name": "Tonga (Tonga Islands)"},
            {"language": "tr", "name": "Turkish"},
            {"language": "ts", "name": "Tsonga"},
            {"language": "tt", "name": "Tatar"},
            {"language": "tw", "name": "Twi"},
            {"language": "ty", "name": "Tahitian"},
            {"language": "ug", "name": "Uighur; Uyghur"},
            {"language": "uk", "name": "Ukrainian"},
            {"language": "ur", "name": "Urdu"},
            {"language": "uz", "name": "Uzbek"},
            {"language": "ve", "name": "Venda"},
            {"language": "vi", "name": "Vietnamese"},
            {"language": "vo", "name": "Volapük"},
            {"language": "wa", "name": "Walloon"},
            {"language": "wo", "name": "Wolof"},
            {"language": "xh", "name": "Xhosa"},
            {"language": "yi", "name": "Yiddish"},
            {"language": "yo", "name": "Yoruba"},
            {"language": "za", "name": "Zhuang; Chuang"},
            {"language": "zh", "name": "Chinese"},
            {"language": "zu", "name": "Zulu"}
        ]

        result_df = pd.DataFrame(blank_list)
        abbr_df = pd.DataFrame(language_abbr)

        df_out = result_df.merge(abbr_df, on='language')
        final_result = df_out.to_dict(orient='records')

        return dumps({'results': final_result})
    except Exception as e:
        return dumps({'err': str(e)})

class YoutubePost(Resource):
    def get(self):
        posts_data = reqparse.RequestParser()
        posts_data.add_argument('page', type=str, required=True, help='Page number is required', location='args')
        posts_data.add_argument('limit', type=str, required=True, help='Limit is required', location='args')
        posts_data.add_argument('sort', type=str, required=False, location='args')
        data = posts_data.parse_args()

        page = data['page']
        page_limit = data['limit']
        sort = data['sort']
        _temp_list = []

        # Total number of posts
        posts_count_cur = main_db.display_youtube_post.aggregate([
            {"$sort": {"datetime": -1}},
            {"$limit": 1},
            {"$unwind": "$data"},
            {"$group": {"_id": "total", "count": {"$sum": {"$toInt": 1}}}}
        ])

        for item in posts_count_cur:
            _temp_list.append(item['count'])

        posts_count = _temp_list[0]

        # Sort By: Date/ Most Likes/ Most Comments
        # case 1: Date
        if (sort == 'date'):
            # fetch all posts
            fetch_posts = main_db.display_youtube_post.aggregate([
                {"$sort": {"datetime": -1}},
                {"$limit": 1},
                {"$unwind": "$data"},
                {"$addFields": {
                    "sub_total": {
                        "$sum": ["$data.like_count", "$data.comment_count"]
                    }
                }},
                {"$addFields": {
                    "eng_rate": {
                        "$divide": ["$sub_total", "$data.view_count"]
                    }
                }},
                {"$addFields": {
                    "former_url": "https://www.youtube.com/watch?v="
                }},
                {"$project": {
                    "_id": 0,
                    "vid": "$vid",
                    "code": "$data.code",
                    "publish_at": {
                        "$dateToString": {
                            "format": "%Y-%m-%d",
                            "date": "$data.publish_at"
                        }
                    },
                    "title": "$data.title",
                    "view_count": "$data.view_count",
                    "like_count": "$data.like_count",
                    "favorite_count": "$data.favorite_count",
                    "comment_count": "$data.comment_count",
                    "tags": "$data.tags",
                    "eng_rate": {
                        "$multiply": ["$eng_rate", 100]
                    },
                    "url": {"$concat": ["$former_url", "$data.code", "/"]},
                    "image": "$data.new_image_url"
                }},
                {"$sort": {"publish_at": -1}},
                {"$skip": int(page_limit) * (int(page) - 1)},
                {"$limit": int(page_limit)}
            ])

            posts_list = []
            for post in fetch_posts:
                posts_list.append(post)

            response = {'total_posts_count': posts_count, 'page': int(page), 'perPage': int(page_limit), 'sort': sort, 'posts': posts_list}

            return {'result': response}
        elif (sort == 'like'):
            fetch_posts = main_db.display_youtube_post.aggregate([
                {"$sort": {"datetime": -1}},
                {"$limit": 1},
                {"$unwind": "$data"},
                {"$addFields": {
                    "sub_total": {
                        "$sum": ["$data.like_count", "$data.comment_count"]
                    }
                }},
                {"$addFields": {
                    "eng_rate": {
                        "$divide": ["$sub_total", "$data.view_count"]
                    }
                }},
                {"$addFields": {
                    "former_url": "https://www.youtube.com/watch?v="
                }},
                {"$project": {
                    "_id": 0,
                    "publish_at": {
                        "$dateToString": {
                            "format": "%Y-%m-%d",
                            "date": "$data.publish_at"
                        }
                    },
                    "title": "$data.title",
                    "code": "$data.code",
                    "view_count": "$data.view_count",
                    "like_count": "$data.like_count",
                    "favorite_count": "$data.favorite_count",
                    "comment_count": "$data.comment_count",
                    "tags": "$data.tags",
                    "eng_rate": {
                        "$multiply": ["$eng_rate", 100]
                    },
                    "url": {"$concat": ["$former_url", "$data.code", "/"]},
                    "image": "$data.new_image_url"
                }},
                {"$sort": {"like_count": -1}},
                {"$skip": int(page_limit) * (int(page) - 1)},
                {"$limit": int(page_limit)}
            ])

            posts_list = []
            for post in fetch_posts:
                posts_list.append(post)

            response = {'total_posts_count': posts_count, 'page': int(page), 'perPage': int(page_limit), 'sort': sort, 'posts': posts_list}

            return {'result': response}

        elif (sort == 'comment'):
            fetch_posts = main_db.display_youtube_post.aggregate([
                {"$sort": {"datetime": -1}},
                {"$limit": 1},
                {"$unwind": "$data"},
                {"$addFields": {
                    "sub_total": {
                        "$sum": ["$data.like_count", "$data.comment_count"]
                    }
                }},
                {"$addFields": {
                    "eng_rate": {
                        "$divide": ["$sub_total", "$data.view_count"]
                    }
                }},
                {"$addFields": {
                    "former_url": "https://www.youtube.com/watch?v="
                }},
                {"$project": {
                    "_id": 0,
                    "publish_at": {
                        "$dateToString": {
                            "format": "%Y-%m-%d",
                            "date": "$data.publish_at"
                        }
                    },
                    "title": "$data.title",
                    "code": "$data.code",
                    "view_count": "$data.view_count",
                    "like_count": "$data.like_count",
                    "favorite_count": "$data.favorite_count",
                    "comment_count": "$data.comment_count",
                    "tags": "$data.tags",
                    "eng_rate": {
                        "$multiply": ["$eng_rate", 100]
                    },
                    "url": {"$concat": ["$former_url", "$data.code", "/"]},
                    "image": "$data.new_image_url"
                }},
                {"$sort": {"comment_count": -1}},
                {"$skip": int(page_limit) * (int(page) - 1)},
                {"$limit": int(page_limit)}
            ])

            posts_list = []
            for post in fetch_posts:
                posts_list.append(post)

            response = {'total_posts_count': posts_count, 'page': int(page), 'perPage': int(page_limit), 'sort': sort, 'posts': posts_list}

            return {'result': response}
        elif (sort == 'engaged'):
            fetch_posts = main_db.display_youtube_post.aggregate([
                {"$sort": {"datetime": -1}},
                {"$limit": 1},
                {"$unwind": "$data"},
                {"$addFields": {
                    "sub_total": {
                        "$sum": ["$data.like_count", "$data.comment_count"]
                    }
                }},
                {"$addFields": {
                    "eng_rate": {
                        "$divide": ["$sub_total", "$data.view_count"]
                    }
                }},
                {"$addFields": {
                    "former_url": "https://www.youtube.com/watch?v="
                }},
                {"$project": {
                    "_id": 0,
                    "publish_at": {
                        "$dateToString": {
                            "format": "%Y-%m-%d",
                            "date": "$data.publish_at"
                        }
                    },
                    "title": "$data.title",
                    "code": "$data.code",
                    "view_count": "$data.view_count",
                    "like_count": "$data.like_count",
                    "favorite_count": "$data.favorite_count",
                    "comment_count": "$data.comment_count",
                    "tags": "$data.tags",
                    "eng_rate": {
                        "$multiply": ["$eng_rate", 100]
                    },
                    "url": {"$concat": ["$former_url", "$data.code", "/"]},
                    "image": "$data.new_image_url"
                }},
                {"$sort": {"eng_rate": -1}},
                {"$skip": int(page_limit) * (int(page) - 1)},
                {"$limit": int(page_limit)}
            ])

            posts_list = []
            for post in fetch_posts:
                posts_list.append(post)

            response = {'total_posts_count': posts_count, 'page': int(page), 'perPage': int(page_limit), 'sort': sort, 'posts': posts_list}

            return {'result': response}
        elif (sort == 'view'):
            fetch_posts = main_db.display_youtube_post.aggregate([
                {"$sort": {"datetime": -1}},
                {"$limit": 1},
                {"$unwind": "$data"},
                {"$addFields": {
                    "sub_total": {
                        "$sum": ["$data.like_count", "$data.comment_count"]
                    }
                }},
                {"$addFields": {
                    "eng_rate": {
                        "$divide": ["$sub_total", "$data.view_count"]
                    }
                }},
                {"$addFields": {
                    "former_url": "https://www.youtube.com/watch?v="
                }},
                {"$project": {
                    "_id": 0,
                    "publish_at": {
                        "$dateToString": {
                            "format": "%Y-%m-%d",
                            "date": "$data.publish_at"
                        }
                    },
                    "title": "$data.title",
                    "code": "$data.code",
                    "view_count": "$data.view_count",
                    "like_count": "$data.like_count",
                    "favorite_count": "$data.favorite_count",
                    "comment_count": "$data.comment_count",
                    "tags": "$data.tags",
                    "eng_rate": {
                        "$multiply": ["$eng_rate", 100]
                    },
                    "url": {"$concat": ["$former_url", "$data.code", "/"]},
                    "image": "$data.new_image_url"
                }},
                {"$sort": {"view_count": -1}},
                {"$skip": int(page_limit) * (int(page) - 1)},
                {"$limit": int(page_limit)}
            ])

            posts_list = []
            for post in fetch_posts:
                posts_list.append(post)

            response = {'total_posts_count': posts_count, 'page': int(page), 'perPage': int(page_limit), 'sort': sort, 'posts': posts_list}

            return {'result': response}
        else:
            # fetch all posts
            fetch_posts = main_db.display_youtube_post.aggregate([
                {"$sort": {"datetime": -1}},
                {"$limit": 1},
                {"$unwind": "$data"},
                {"$addFields": {
                    "sub_total": {
                        "$sum": ["$data.like_count", "$data.comment_count"]
                    }
                }},
                {"$addFields": {
                    "eng_rate": {
                        "$divide": ["$sub_total", "$data.view_count"]
                    }
                }},
                {"$addFields": {
                    "former_url": "https://www.youtube.com/watch?v="
                }},
                {"$project": {
                    "_id": 0,
                    "publish_at": {
                        "$dateToString": {
                            "format": "%Y-%m-%d",
                            "date": "$data.publish_at"
                        }
                    },
                    "title": "$data.title",
                    "code": "$data.code",
                    "view_count": "$data.view_count",
                    "like_count": "$data.like_count",
                    "favorite_count": "$data.favorite_count",
                    "comment_count": "$data.comment_count",
                    "tags": "$data.tags",
                    "eng_rate": {
                        "$multiply": ["$eng_rate", 100]
                    },
                    "url": {"$concat": ["$former_url", "$data.code", "/"]},
                    "image": "$data.new_image_url"
                }},
                {"$sort": {"publish_at": -1}},
                {"$skip": int(page_limit) * (int(page) - 1)},
                {"$limit": int(page_limit)}
            ])

            posts_list = []
            for post in fetch_posts:
                posts_list.append(post)

            response = {'total_posts_count': posts_count, 'page': int(page), 'perPage': int(page_limit), 'sort': sort, 'posts': posts_list}

            return {'result': response}

# YouTube most-used hashtags
class YoutubeUsedTags(Resource):
    def get(self):
        posts_data = reqparse.RequestParser()
        posts_data.add_argument('latest', type=str, required=False, help='Limit is required', location='args')
        data = posts_data.parse_args()

        latest = data['latest']
        _temp_count_list = []

        # Total number of posts
        posts_count_cur = main_db.youtube_video_info.aggregate([
            {"$sort": {"datetime": -1}},
            {"$limit": 1},
            {"$unwind": "$video_data"},
            {"$group": {"_id": "total", "count": {"$sum": {"$toInt": 1}}}}
        ])

        for item in posts_count_cur:
            _temp_count_list.append(item['count'])

        posts_count = _temp_count_list[0]

        # Sort By: Latest 10, 30, all posts
        # case 1: Latest 10
        if (latest == 'ten'):
            results = main_db.youtube_video_info.aggregate([
                {"$sort": {"datetime": -1}},
                {"$limit": 1},
                {"$unwind": "$video_data"},
                {"$limit": 10},
                {"$project": {
                    "_id": 0,
                    "published_date": "$video_data.publishedAt",
                    "title": "$video_data.title",
                    "tags": "$video_data.tags"
                }},
                {"$set": {
                    "n": {
                        "$replaceOne": {
                            "input": "$title",
                            "find": "#",
                            "replacement": " #"
                        }
                    }}
                }
            ])
            _temp_list = []
            for item in results:
                _temp_list.append(item)

            # flatten item in list
            _tag = [ele.get("tags") for ele in _temp_list]
            _title = [extract_hashtags_keyword(ele["n"]) for ele in _temp_list]
            # print(_title)
            # print(_tag)
            flat_title = [item for sublist in _title for item in sublist]
            # print(flat_title)

            # replace None value to ''
            _switch_none = ['' if v is None else v for v in _tag]
            # flatten tags list
            flat_tag = [item for sublist in _switch_none for item in sublist]
            # print(flat_tag)

            # concatenate two lists, and count occurrence value
            joined_list = flat_title + flat_tag
            w = pd.value_counts(np.array(joined_list))

            # convert list to df then dict
            df = pd.DataFrame(list(zip(w.keys(), w)), columns=['hashtag', 'count'])
            result = df.to_dict(orient='records')[:10]

            response = {'total_posts_count': posts_count, 'latest': latest, 'posts': result}

            return {'result': response}
        elif (latest == 'thirty'):
            results = main_db.youtube_video_info.aggregate([
                {"$sort": {"datetime": -1}},
                {"$limit": 1},
                {"$unwind": "$video_data"},
                {"$limit": 30},
                {"$project": {
                    "_id": 0,
                    "published_date": "$video_data.publishedAt",
                    "title": "$video_data.title",
                    "tags": "$video_data.tags"
                }},
                {"$set": {
                    "n": {
                        "$replaceOne": {
                            "input": "$title",
                            "find": "#",
                            "replacement": " #"
                        }
                    }}
                }
            ])
            _temp_list = []
            for item in results:
                _temp_list.append(item)

            # flatten item in list
            _tag = [ele.get("tags") for ele in _temp_list]
            _title = [extract_hashtags_keyword(ele["n"]) for ele in _temp_list]
            # print(_title)
            # print(_tag)
            flat_title = [item for sublist in _title for item in sublist]
            # print(flat_title)

            # replace None value to ''
            _switch_none = ['' if v is None else v for v in _tag]
            # flatten tags list
            flat_tag = [item for sublist in _switch_none for item in sublist]
            # print(flat_tag)

            # concatenate two lists, and count occurrence value
            joined_list = flat_title + flat_tag
            w = pd.value_counts(np.array(joined_list))

            # convert list to df then dict
            df = pd.DataFrame(list(zip(w.keys(), w)), columns=['hashtag', 'count'])
            result = df.to_dict(orient='records')[:10]

            response = {'total_posts_count': posts_count, 'latest': latest, 'posts': result}

            return {'result': response}
        elif (latest == 'all'):
            results = main_db.youtube_video_info.aggregate([
                {"$sort": {"datetime": -1}},
                {"$limit": 1},
                {"$unwind": "$video_data"},
                {"$project": {
                    "_id": 0,
                    "published_date": "$video_data.publishedAt",
                    "title": "$video_data.title",
                    "tags": "$video_data.tags"
                }},
                {"$set": {
                    "n": {
                        "$replaceOne": {
                            "input": "$title",
                            "find": "#",
                            "replacement": " #"
                        }
                    }}
                }
            ])
            _temp_list = []
            for item in results:
                _temp_list.append(item)

            # flatten item in list
            _tag = [ele.get("tags") for ele in _temp_list]
            _title = [extract_hashtags_keyword(ele["n"]) for ele in _temp_list]
            # print(_title)
            # print(_tag)
            flat_title = [item for sublist in _title for item in sublist]
            # print(flat_title)

            # replace None value to ''
            _switch_none = ['' if v is None else v for v in _tag]
            # flatten tags list
            flat_tag = [item for sublist in _switch_none for item in sublist]
            # print(flat_tag)

            # concatenate two lists, and count occurrence value
            joined_list = flat_title + flat_tag
            w = pd.value_counts(np.array(joined_list))

            # convert list to df then dict
            df = pd.DataFrame(list(zip(w.keys(), w)), columns=['hashtag', 'count'])
            result = df.to_dict(orient='records')[:10]

            response = {'total_posts_count': posts_count, 'latest': latest, 'posts': result}

            return {'result': response}
        else: # return latest 10
            results = main_db.youtube_video_info.aggregate([
                {"$sort": {"datetime": -1}},
                {"$limit": 1},
                {"$unwind": "$video_data"},
                {"$limit": 10},
                {"$project": {
                    "_id": 0,
                    "published_date": "$video_data.publishedAt",
                    "title": "$video_data.title",
                    "tags": "$video_data.tags"
                }},
                {"$set": {
                    "n": {
                        "$replaceOne": {
                            "input": "$title",
                            "find": "#",
                            "replacement": " #"
                        }
                    }}
                }
            ])
            _temp_list = []
            for item in results:
                _temp_list.append(item)

            # flatten item in list
            _tag = [ele.get("tags") for ele in _temp_list]
            _title = [extract_hashtags_keyword(ele["n"]) for ele in _temp_list]
            # print(_title)
            # print(_tag)
            flat_title = [item for sublist in _title for item in sublist]
            # print(flat_title)

            # replace None value to ''
            _switch_none = ['' if v is None else v for v in _tag]
            # flatten tags list
            flat_tag = [item for sublist in _switch_none for item in sublist]
            # print(flat_tag)

            # concatenate two lists, and count occurrence value
            joined_list = flat_title + flat_tag
            w = pd.value_counts(np.array(joined_list))

            # convert list to df then dict
            df = pd.DataFrame(list(zip(w.keys(), w)), columns=['hashtag', 'count'])
            result = df.to_dict(orient='records')[:10]

            response = {'total_posts_count': posts_count, 'latest': latest, 'posts': result}

            return {'result': response}

# YouTube most-engaged hashtags
class YoutubeEngagedTags(Resource):
    def get(self):
        posts_data = reqparse.RequestParser()
        posts_data.add_argument('latest', type=str, required=False, help='Limit is required', location='args')
        data = posts_data.parse_args()

        latest = data['latest']
        _temp_count_list = []

        # Total number of posts
        posts_count_cur = main_db.youtube_video_info.aggregate([
            {"$sort": {"datetime": -1}},
            {"$limit": 1},
            {"$unwind": "$video_data"},
            {"$group": {"_id": "total", "count": {"$sum": {"$toInt": 1}}}}
        ])

        for item in posts_count_cur:
            _temp_count_list.append(item['count'])

        posts_count = _temp_count_list[0]

        # Sort By: Latest 10, 30, all posts
        # case 1: Latest 10
        if (latest == 'ten'):
            results = main_db.youtube_video_info.aggregate([
                {"$sort": {"datetime": -1}},
                {"$limit": 1},
                {"$unwind": "$video_data"},
                {"$project": {
                    "_id": 0,
                    "date": "$datetime",
                    "publishedAt": "$video_data.publishedAt",
                    "title": "$video_data.title",
                    "tags": "$video_data.tags",
                    "desc": "$video_data.description",
                    "viewCount": "$video_data.viewCount",
                    "likeCount": "$video_data.likeCount",
                    "favoriteCount": "$video_data.favoriteCount",
                    "commentCount": "$video_data.commentCount"
                }},
                {"$lookup": {
                    "from": "youtube_index",
                    "localField": "date",
                    "foreignField": "datetime",
                    "as": "y_info"
                }},
                {"$project": {
                    "_id": 0,
                    "date": "$date",
                    "publishedAt": "$publishedAt",
                    "title": "$title",
                    "tags": "$tags",
                    "viewCount": "$viewCount",
                    "likeCount": "$likeCount",
                    "favoriteCount": "$favoriteCount",
                    "commentCount": "$commentCount",
                    "subscriber": {"$slice": ["$y_info.data.subscriberCount", -1]}
                }},
                {"$unwind": "$subscriber"},
                {"$set": {
                    "n": {
                        "$replaceOne": {
                            "input": "$title",
                            "find": "#",
                            "replacement": " #"
                        }
                    }}
                },
                {"$project": {
                    "date": "$date",
                    "publishedAt": "$publishedAt",
                    "title": "$title",
                    "tags": "$tags",
                    "viewCount": "$viewCount",
                    "likeCount": "$likeCount",
                    "favoriteCount": "$favoriteCount",
                    "commentCount": "$commentCount",
                    "subscriber": "$subscriber",
                    "nn": {
                        "$split": ["$n", " "]
                    }
                }},
                {"$sort": {"publishedAt": -1}},
                {"$limit": 10},
                {"$unwind": "$nn"},
                {"$addFields": {
                    "_cleaned": {
                        "$regexFindAll": {
                            "input": "$nn",
                            "regex": "#.*"
                        }
                    }
                }},
                # concat two arrays
                {"$project": {
                    "date": "$date",
                    "publishedAt": "$publishedAt",
                    "title": "$title",
                    "tags": "$tags",
                    "viewCount": {"$toInt": "$viewCount"},
                    "likeCount": {"$toInt": "$likeCount"},
                    "favoriteCount": {"$toInt": "$favoriteCount"},
                    "commentCount": {"$toInt": "$commentCount"},
                    "subscriber": "$subscriber",
                    "_new": {
                        "$concatArrays": [
                            {"$ifNull": ["$_cleaned.match", []]},
                            {"$ifNull": ["$tags", []]}
                        ]
                    }
                }},
                # add subtotal: likes+comment
                {"$addFields": {
                    "sub_total": {
                        "$sum": ["$likeCount", "$commentCount"]
                    }
                }},
                {"$unwind": "$_new"},
                {"$addFields": {
                    "_eng_rate": {"$divide": ["$sub_total", "$viewCount"]}
                }},
                # groupby hashtag
                {"$group": {
                    "_id": "$_new",
                    "count": {"$sum": 1},
                    "_total_eng_rate": {"$sum": "$_eng_rate"}
                }},
                {"$project": {
                    "eng_rate_per_hashtag": {
                        "$divide": ["$_total_eng_rate", "$count"]
                    }
                }},
                {"$project": {
                    "eng_rate_per_hashtag": {
                        "$multiply": ["$eng_rate_per_hashtag", 100]
                    }
                }},
                {"$sort": {"eng_rate_per_hashtag": -1}},
                {"$limit": 10}
            ])

            posts_list = []
            for post in results:
                posts_list.append(post)

            response = {'total_posts_count': posts_count, 'latest': latest, 'posts': posts_list}

            return {'result': response}
        elif (latest == 'thirty'):
            results = main_db.youtube_video_info.aggregate([
                {"$sort": {"datetime": -1}},
                {"$limit": 1},
                {"$unwind": "$video_data"},
                {"$project": {
                    "_id": 0,
                    "date": "$datetime",
                    "publishedAt": "$video_data.publishedAt",
                    "title": "$video_data.title",
                    "tags": "$video_data.tags",
                    "desc": "$video_data.description",
                    "viewCount": "$video_data.viewCount",
                    "likeCount": "$video_data.likeCount",
                    "favoriteCount": "$video_data.favoriteCount",
                    "commentCount": "$video_data.commentCount"
                }},
                {"$lookup": {
                    "from": "youtube_index",
                    "localField": "date",
                    "foreignField": "datetime",
                    "as": "y_info"
                }},
                {"$project": {
                    "_id": 0,
                    "date": "$date",
                    "publishedAt": "$publishedAt",
                    "title": "$title",
                    "tags": "$tags",
                    "viewCount": "$viewCount",
                    "likeCount": "$likeCount",
                    "favoriteCount": "$favoriteCount",
                    "commentCount": "$commentCount",
                    "subscriber": {"$slice": ["$y_info.data.subscriberCount", -1]}
                }},
                {"$unwind": "$subscriber"},
                {"$set": {
                    "n": {
                        "$replaceOne": {
                            "input": "$title",
                            "find": "#",
                            "replacement": " #"
                        }
                    }}
                },
                {"$project": {
                    "date": "$date",
                    "publishedAt": "$publishedAt",
                    "title": "$title",
                    "tags": "$tags",
                    "viewCount": "$viewCount",
                    "likeCount": "$likeCount",
                    "favoriteCount": "$favoriteCount",
                    "commentCount": "$commentCount",
                    "subscriber": "$subscriber",
                    "nn": {
                        "$split": ["$n", " "]
                    }
                }},
                {"$sort": {"publishedAt": -1}},
                {"$limit": 30},
                {"$unwind": "$nn"},
                {"$addFields": {
                    "_cleaned": {
                        "$regexFindAll": {
                            "input": "$nn",
                            "regex": "#.*"
                        }
                    }
                }},
                # concat two arrays
                {"$project": {
                    "date": "$date",
                    "publishedAt": "$publishedAt",
                    "title": "$title",
                    "tags": "$tags",
                    "viewCount": {"$toInt": "$viewCount"},
                    "likeCount": {"$toInt": "$likeCount"},
                    "favoriteCount": {"$toInt": "$favoriteCount"},
                    "commentCount": {"$toInt": "$commentCount"},
                    "subscriber": "$subscriber",
                    "_new": {
                        "$concatArrays": [
                            {"$ifNull": ["$_cleaned.match", []]},
                            {"$ifNull": ["$tags", []]}
                        ]
                    }
                }},
                # add subtotal: likes+comment
                {"$addFields": {
                    "sub_total": {
                        "$sum": ["$likeCount", "$commentCount"]
                    }
                }},
                {"$unwind": "$_new"},
                {"$addFields": {
                    "_eng_rate": {"$divide": ["$sub_total", "$viewCount"]}
                }},
                # groupby hashtag
                {"$group": {
                    "_id": "$_new",
                    "count": {"$sum": 1},
                    "_total_eng_rate": {"$sum": "$_eng_rate"}
                }},
                {"$project": {
                    "eng_rate_per_hashtag": {
                        "$divide": ["$_total_eng_rate", "$count"]
                    }
                }},
                {"$project": {
                    "eng_rate_per_hashtag": {
                        "$multiply": ["$eng_rate_per_hashtag", 100]
                    }
                }},
                {"$sort": {"eng_rate_per_hashtag": -1}},
                {"$limit": 10}
            ])

            posts_list = []
            for post in results:
                posts_list.append(post)

            response = {'total_posts_count': posts_count, 'latest': latest, 'posts': posts_list}

            return {'result': response}
        elif (latest == 'all'):
            results = main_db.youtube_video_info.aggregate([
                {"$sort": {"datetime": -1}},
                {"$limit": 1},
                {"$unwind": "$video_data"},
                {"$project": {
                    "_id": 0,
                    "date": "$datetime",
                    "publishedAt": "$video_data.publishedAt",
                    "title": "$video_data.title",
                    "tags": "$video_data.tags",
                    "desc": "$video_data.description",
                    "viewCount": "$video_data.viewCount",
                    "likeCount": "$video_data.likeCount",
                    "favoriteCount": "$video_data.favoriteCount",
                    "commentCount": "$video_data.commentCount"
                }},
                {"$lookup": {
                    "from": "youtube_index",
                    "localField": "date",
                    "foreignField": "datetime",
                    "as": "y_info"
                }},
                {"$project": {
                    "_id": 0,
                    "date": "$date",
                    "publishedAt": "$publishedAt",
                    "title": "$title",
                    "tags": "$tags",
                    "viewCount": "$viewCount",
                    "likeCount": "$likeCount",
                    "favoriteCount": "$favoriteCount",
                    "commentCount": "$commentCount",
                    "subscriber": {"$slice": ["$y_info.data.subscriberCount", -1]}
                }},
                {"$unwind": "$subscriber"},
                {"$set": {
                    "n": {
                        "$replaceOne": {
                            "input": "$title",
                            "find": "#",
                            "replacement": " #"
                        }
                    }}
                },
                {"$project": {
                    "date": "$date",
                    "publishedAt": "$publishedAt",
                    "title": "$title",
                    "tags": "$tags",
                    "viewCount": "$viewCount",
                    "likeCount": "$likeCount",
                    "favoriteCount": "$favoriteCount",
                    "commentCount": "$commentCount",
                    "subscriber": "$subscriber",
                    "nn": {
                        "$split": ["$n", " "]
                    }
                }},
                {"$sort": {"publishedAt": -1}},
                {"$unwind": "$nn"},
                {"$addFields": {
                    "_cleaned": {
                        "$regexFindAll": {
                            "input": "$nn",
                            "regex": "#.*"
                        }
                    }
                }},
                # concat two arrays
                {"$project": {
                    "date": "$date",
                    "publishedAt": "$publishedAt",
                    "title": "$title",
                    "tags": "$tags",
                    "viewCount": {"$toInt": "$viewCount"},
                    "likeCount": {"$toInt": "$likeCount"},
                    "favoriteCount": {"$toInt": "$favoriteCount"},
                    "commentCount": {"$toInt": "$commentCount"},
                    "subscriber": "$subscriber",
                    "_new": {
                        "$concatArrays": [
                            {"$ifNull": ["$_cleaned.match", []]},
                            {"$ifNull": ["$tags", []]}
                        ]
                    }
                }},
                # add subtotal: likes+comment
                {"$addFields": {
                    "sub_total": {
                        "$sum": ["$likeCount", "$commentCount"]
                    }
                }},
                {"$unwind": "$_new"},
                {"$addFields": {
                    "_eng_rate": {"$divide": ["$sub_total", "$viewCount"]}
                }},
                # groupby hashtag
                {"$group": {
                    "_id": "$_new",
                    "count": {"$sum": 1},
                    "_total_eng_rate": {"$sum": "$_eng_rate"}
                }},
                {"$project": {
                    "eng_rate_per_hashtag": {
                        "$divide": ["$_total_eng_rate", "$count"]
                    }
                }},
                {"$project": {
                    "eng_rate_per_hashtag": {
                        "$multiply": ["$eng_rate_per_hashtag", 100]
                    }
                }},
                {"$sort": {"eng_rate_per_hashtag": -1}},
                {"$limit": 10}
            ])

            posts_list = []
            for post in results:
                posts_list.append(post)

            response = {'total_posts_count': posts_count, 'latest': latest, 'posts': posts_list}

            return {'result': response}
        else: # return latest 10 posts
            results = main_db.youtube_video_info.aggregate([
                {"$sort": {"datetime": -1}},
                {"$limit": 1},
                {"$unwind": "$video_data"},
                {"$project": {
                    "_id": 0,
                    "date": "$datetime",
                    "publishedAt": "$video_data.publishedAt",
                    "title": "$video_data.title",
                    "tags": "$video_data.tags",
                    "desc": "$video_data.description",
                    "viewCount": "$video_data.viewCount",
                    "likeCount": "$video_data.likeCount",
                    "favoriteCount": "$video_data.favoriteCount",
                    "commentCount": "$video_data.commentCount"
                }},
                {"$lookup": {
                    "from": "youtube_index",
                    "localField": "date",
                    "foreignField": "datetime",
                    "as": "y_info"
                }},
                {"$project": {
                    "_id": 0,
                    "date": "$date",
                    "publishedAt": "$publishedAt",
                    "title": "$title",
                    "tags": "$tags",
                    "viewCount": "$viewCount",
                    "likeCount": "$likeCount",
                    "favoriteCount": "$favoriteCount",
                    "commentCount": "$commentCount",
                    "subscriber": {"$slice": ["$y_info.data.subscriberCount", -1]}
                }},
                {"$unwind": "$subscriber"},
                {"$set": {
                    "n": {
                        "$replaceOne": {
                            "input": "$title",
                            "find": "#",
                            "replacement": " #"
                        }
                    }}
                },
                {"$project": {
                    "date": "$date",
                    "publishedAt": "$publishedAt",
                    "title": "$title",
                    "tags": "$tags",
                    "viewCount": "$viewCount",
                    "likeCount": "$likeCount",
                    "favoriteCount": "$favoriteCount",
                    "commentCount": "$commentCount",
                    "subscriber": "$subscriber",
                    "nn": {
                        "$split": ["$n", " "]
                    }
                }},
                {"$sort": {"publishedAt": -1}},
                {"$limit": 10},
                {"$unwind": "$nn"},
                {"$addFields": {
                    "_cleaned": {
                        "$regexFindAll": {
                            "input": "$nn",
                            "regex": "#.*"
                        }
                    }
                }},
                # concat two arrays
                {"$project": {
                    "date": "$date",
                    "publishedAt": "$publishedAt",
                    "title": "$title",
                    "tags": "$tags",
                    "viewCount": {"$toInt": "$viewCount"},
                    "likeCount": {"$toInt": "$likeCount"},
                    "favoriteCount": {"$toInt": "$favoriteCount"},
                    "commentCount": {"$toInt": "$commentCount"},
                    "subscriber": "$subscriber",
                    "_new": {
                        "$concatArrays": [
                            {"$ifNull": ["$_cleaned.match", []]},
                            {"$ifNull": ["$tags", []]}
                        ]
                    }
                }},
                # add subtotal: likes+comment
                {"$addFields": {
                    "sub_total": {
                        "$sum": ["$likeCount", "$commentCount"]
                    }
                }},
                {"$unwind": "$_new"},
                {"$addFields": {
                    "_eng_rate": {"$divide": ["$sub_total", "$viewCount"]}
                }},
                # groupby hashtag
                {"$group": {
                    "_id": "$_new",
                    "count": {"$sum": 1},
                    "_total_eng_rate": {"$sum": "$_eng_rate"}
                }},
                {"$project": {
                    "eng_rate_per_hashtag": {
                        "$divide": ["$_total_eng_rate", "$count"]
                    }
                }},
                {"$project": {
                    "eng_rate_per_hashtag": {
                        "$multiply": ["$eng_rate_per_hashtag", 100]
                    }
                }},
                {"$sort": {"eng_rate_per_hashtag": -1}},
                {"$limit": 10}
            ])

            posts_list = []
            for post in results:
                posts_list.append(post)

            response = {'total_posts_count': posts_count, 'latest': latest, 'posts': posts_list}

            return {'result': response}


class YoutubeComment(Resource):
    def get(self):
        posts_data = reqparse.RequestParser()
        posts_data.add_argument('page', type=int, required=True, help='Page number is required', location='args')
        posts_data.add_argument('limit', type=int, required=True, help='Limit is required', location='args')
        posts_data.add_argument('drange', type=int, required=False, location='args')
        data = posts_data.parse_args()

        page = data['page']
        page_limit = data['limit']
        drange = data['drange']
        _temp_list = []

        # Total number of posts
        posts_count_cur = main_db.display_youtube_post.aggregate([
            {"$sort": {"datetime": -1}},
            {"$limit": 1},
            {"$unwind": "$data"},
            {"$group": {"_id": "total", "count": {"$sum": {"$toInt": 1}}}}
        ])

        for item in posts_count_cur:
            _temp_list.append(item['count'])

        posts_count = _temp_list[0]

        # Sort By: Latest 10/ 30/
        # case 1: Latest 10
        if (drange == 10):
            # fetch all posts
            fetch_posts = main_db.youtube_comment.aggregate([
                # find the max score label from each comment
                {"$addFields": {"sentiment": {"$reduce": {
                    "input": "$sentiment",
                    "initialValue": {"score": 0},
                    "in": {"$cond": [{"$gte": ["$$this.score", "$$value.score"]}, "$$this", "$$value"]}}
                }}},
                {"$project": {
                    "video_id": "$video_id",
                    "comment_id": "$comment_id",
                    "comment_text": "$comment_text",
                    "like_count": "$like_count",
                    "author": "$author",
                    "author_profile_image": "$author_profile_image",
                    "author_channel_id": "$author_channel_id",
                    "published_at": "$published_at",
                    "updated_at": "$updated_at",
                    "language": "$language",
                    "label": "$sentiment.label",
                    "score": "$sentiment.score"
                }},
                {"$group": {
                    "_id": "$video_id",
                    "list": {
                        "$push": "$$ROOT"
                    }
                }},
                # get latest 10 comments of each video
                {"$project": {
                    "latest_ten": {
                        "$slice": ["$list", drange]
                    }
                }},
                {"$unwind": "$latest_ten"},
                # group bt video id and label to get the count first
                {"$group": {
                    "_id": {
                        "video_id": "$_id",
                        "label": "$latest_ten.label",
                    },
                    "datetime": {"$first": "$latest_ten.published_at"},
                    "count": {"$sum": {"$toInt": 1}}
                    # "comment_id": {"$first": "$list.comment_id"},
                    # "comment": {"$first": "$list.comment_text"},
                    # "count": {"$sum": {"$toInt": 1}},
                    # "updated_at": {"$first": "$list.updated_at"},
                    # "published_at": {"$first": "$list.published_at"}
                }},
                {"$group": {
                    "_id": "$_id.video_id",
                    "datetime": {"$first": "$datetime"},
                    "count": {
                        "$addToSet": {
                            "k": "$_id.label",
                            "v": "$count"
                        }
                    }
                }},
                {"$project": {
                    "datetime": "$datetime",
                    "count": {
                        "$arrayToObject": "$count"
                    }
                }},
                {"$project": {
                    "vid": "$_id",
                    "datetime": "$datetime",
                    "pos": "$count.Positive",
                    "neg": "$count.Negative",
                    "neu": "$count.Neutral",
                    "total": {"$sum": ["$count.Positive", "$count.Negative", "$count.Neutral"]}
                }},
                {"$project": {
                    "vid": "$vid",
                    "datetime": "$datetime",
                    "pos_perc": {
                        "$round": [{"$multiply": [{"$divide": ["$pos", "$total"]}, 100]}, 2]
                    },
                    "neg_perc": {
                        "$round": [{"$multiply": [{"$divide": ["$neg", "$total"]}, 100]}, 2]
                    },
                    "neu_perc": {
                        "$round": [{"$multiply": [{"$divide": ["$neu", "$total"]}, 100]}, 2]
                    },
                }},
                {"$sort": {"datetime": -1}},
                {"$skip": int(page_limit) * (int(page) - 1)},
                {"$limit": int(page_limit)}
            ])

            posts_list = []
            for post in fetch_posts:
                posts_list.append(post)

            response = {'total_posts_count': posts_count,
                        'page': int(page),
                        'perPage': int(page_limit),
                        'drange': drange,
                        'posts': posts_list}

            return {'result': response}
        elif (drange == 30):
            # fetch all posts
            fetch_posts = main_db.youtube_comment.aggregate([
                # find the max score label from each comment
                {"$addFields": {"sentiment": {"$reduce": {
                    "input": "$sentiment",
                    "initialValue": {"score": 0},
                    "in": {"$cond": [{"$gte": ["$$this.score", "$$value.score"]}, "$$this", "$$value"]}}
                }}},
                {"$project": {
                    "video_id": "$video_id",
                    "comment_id": "$comment_id",
                    "comment_text": "$comment_text",
                    "like_count": "$like_count",
                    "author": "$author",
                    "author_profile_image": "$author_profile_image",
                    "author_channel_id": "$author_channel_id",
                    "published_at": "$published_at",
                    "updated_at": "$updated_at",
                    "language": "$language",
                    "label": "$sentiment.label",
                    "score": "$sentiment.score"
                }},
                {"$group": {
                    "_id": "$video_id",
                    "list": {
                        "$push": "$$ROOT"
                    }
                }},
                # get latest 10 comments of each video
                {"$project": {
                    "latest_ten": {
                        "$slice": ["$list", drange]
                    }
                }},
                {"$unwind": "$latest_ten"},
                # group bt video id and label to get the count first
                {"$group": {
                    "_id": {
                        "video_id": "$_id",
                        "label": "$latest_ten.label",
                    },
                    "datetime": {"$first": "$latest_ten.published_at"},
                    "count": {"$sum": {"$toInt": 1}}
                    # "comment_id": {"$first": "$list.comment_id"},
                    # "comment": {"$first": "$list.comment_text"},
                    # "count": {"$sum": {"$toInt": 1}},
                    # "updated_at": {"$first": "$list.updated_at"},
                    # "published_at": {"$first": "$list.published_at"}
                }},
                {"$group": {
                    "_id": "$_id.video_id",
                    "datetime": {"$first": "$datetime"},
                    "count": {
                        "$addToSet": {
                            "k": "$_id.label",
                            "v": "$count"
                        }
                    }
                }},
                {"$project": {
                    "datetime": "$datetime",
                    "count": {
                        "$arrayToObject": "$count"
                    }
                }},
                {"$project": {
                    "vid": "$_id",
                    "datetime": "$datetime",
                    "pos": "$count.Positive",
                    "neg": "$count.Negative",
                    "neu": "$count.Neutral",
                    "total": {"$sum": ["$count.Positive", "$count.Negative", "$count.Neutral"]}
                }},
                {"$project": {
                    "vid": "$vid",
                    "datetime": "$datetime",
                    "pos_perc": {
                        "$round": [{"$multiply": [{"$divide": ["$pos", "$total"]}, 100]}, 2]
                    },
                    "neg_perc": {
                        "$round": [{"$multiply": [{"$divide": ["$neg", "$total"]}, 100]}, 2]
                    },
                    "neu_perc": {
                        "$round": [{"$multiply": [{"$divide": ["$neu", "$total"]}, 100]}, 2]
                    },
                }},
                {"$sort": {"datetime": -1}},
                {"$skip": int(page_limit) * (int(page) - 1)},
                {"$limit": int(page_limit)}
            ])

            posts_list = []
            for post in fetch_posts:
                posts_list.append(post)

            response = {'total_posts_count': posts_count, 'page': int(page), 'perPage': int(page_limit), 'drange': drange, 'posts': posts_list}

            return {'result': response}
        else:
            # fetch all posts
            fetch_posts = main_db.youtube_comment.aggregate([
                # find the max score label from each comment
                {"$addFields": {"sentiment": {"$reduce": {
                    "input": "$sentiment",
                    "initialValue": {"score": 0},
                    "in": {"$cond": [{"$gte": ["$$this.score", "$$value.score"]}, "$$this", "$$value"]}}
                }}},
                {"$project": {
                    "video_id": "$video_id",
                    "comment_id": "$comment_id",
                    "comment_text": "$comment_text",
                    "like_count": "$like_count",
                    "author": "$author",
                    "author_profile_image": "$author_profile_image",
                    "author_channel_id": "$author_channel_id",
                    "published_at": "$published_at",
                    "updated_at": "$updated_at",
                    "language": "$language",
                    "label": "$sentiment.label",
                    "score": "$sentiment.score"
                }},
                {"$group": {
                    "_id": "$video_id",
                    "list": {
                        "$push": "$$ROOT"
                    }
                }},
                # get latest 10 comments of each video
                {"$project": {
                    "latest_ten": {
                        "$slice": ["$list", 10]
                    }
                }},
                {"$unwind": "$latest_ten"},
                # group bt video id and label to get the count first
                {"$group": {
                    "_id": {
                        "video_id": "$_id",
                        "label": "$latest_ten.label",
                    },
                    "datetime": {"$first": "$latest_ten.published_at"},
                    "count": {"$sum": {"$toInt": 1}}
                    # "comment_id": {"$first": "$list.comment_id"},
                    # "comment": {"$first": "$list.comment_text"},
                    # "count": {"$sum": {"$toInt": 1}},
                    # "updated_at": {"$first": "$list.updated_at"},
                    # "published_at": {"$first": "$list.published_at"}
                }},
                {"$group": {
                    "_id": "$_id.video_id",
                    "datetime": {"$first": "$datetime"},
                    "count": {
                        "$addToSet": {
                            "k": "$_id.label",
                            "v": "$count"
                        }
                    }
                }},
                {"$project": {
                    "datetime": "$datetime",
                    "count": {
                        "$arrayToObject": "$count"
                    }
                }},
                {"$project": {
                    "vid": "$_id",
                    "datetime": "$datetime",
                    "pos": "$count.Positive",
                    "neg": "$count.Negative",
                    "neu": "$count.Neutral",
                    "total": {"$sum": ["$count.Positive", "$count.Negative", "$count.Neutral"]}
                }},
                {"$project": {
                    "vid": "$vid",
                    "datetime": "$datetime",
                    "pos_perc": {
                        "$round": [{"$multiply": [{"$divide": ["$pos", "$total"]}, 100]}, 2]
                    },
                    "neg_perc": {
                        "$round": [{"$multiply": [{"$divide": ["$neg", "$total"]}, 100]}, 2]
                    },
                    "neu_perc": {
                        "$round": [{"$multiply": [{"$divide": ["$neu", "$total"]}, 100]}, 2]
                    },
                }},
                {"$sort": {"datetime": -1}},
                {"$skip": int(page_limit) * (int(page) - 1)},
                {"$limit": int(page_limit)}
            ])
            posts_list = []
            for post in fetch_posts:
                posts_list.append(post)

            response = {'total_posts_count': posts_count, 'page': int(page), 'perPage': int(page_limit), 'drange': drange, 'posts': posts_list}

            return {'result': response}


class YoutubeEngagementRate(Resource):
    def get(self):
        pass
        # TODO ENG RATE CALCULATE
        # db.youtube_video_info.aggregate([
        #     {"$sort": {"datetime": -1}},
        #     {"$limit": 30},
        #     {"$project": {
        #         "datetime": "$datetime",
        #         "video_data": {"$slice": ["$video_data", 10]}
        #     }},
        #     {"$unwind": "$video_data"},
        #     {"$project": {
        #         "_id": 0,
        #         "datetime": "$datetime",
        #         "title": "$video_data.title",
        #         "published_at": "$video_data.publishedAt",
        #         "view_count": {"$toInt": "$video_data.viewCount"},
        #         "like_count": {"$toInt": "$video_data.likeCount"},
        #         "favorite_count": {"$toInt": "$video_data.favoriteCount"},
        #         "comment_count": {"$toInt": "$video_data.commentCount"}
        #     }},
        #     {"$addFields": {
        #         "sub_total": {
        #             "$sum": ["$like_count", "$comment_count", "$favorite_count"]}
        #     }},
        #     {"$addFields": {
        #         "eng_rate": {
        #             "$round": [
        #                 {"$multiply": [{"$divide": ["$sub_total", "$view_count"]}, 100]}, 2
        #             ]
        #         }
        #     }},
        #     {"$group": {
        #         "_id": "$datetime",
        #         "tot_eng_rate": {"$sum": "$eng_rate"},
        #         "video_num": {"$sum": {"$toInt": 1}}
        #     }},
        #     {"$sort": {"_id": -1}},
        #     {"$project": {
        #         "avg_eng_rate": {
        #             "$round": [
        #                 {"$divide": ["$tot_eng_rate", "$video_num"]}, 2
        #             ]}
        #     }}
        # ])


class LatestTenPostEngagementRate(Resource):
    def get(self):
        pass
        # db.instagram_post_info.aggregate([
        #     {"$sort": {"date": -1}},
        #     {"$limit": 1},
        #     {"$unwind": "$post"},
        #     {"$project": {
        #         "_id": 0,
        #         "date": "$date",
        #         "post_date": "$post.taken_at",
        #         "title": "$post.caption_text",
        #         "comment_count": "$post.comment_count",
        #         "like_count": "$post.like_count",
        #         "hashtags": "$post.hashtags",
        #         "image": "$post.thumbnail_url",
        #         "code": "$post.code",
        #         "cat": "$post.cat",
        #         "follower": "$follower_count"
        #     }},
        #     {"$addFields": {
        #         "sub_total": {
        #             "$sum": ["$comment_count", "$like_count"]}
        #     }},
        #     {"$sort": {"post_date": -1}},
        #     {"$limit": 10},
        #     {"$addFields": {
        #         "eng_rate": {
        #             "$divide": ["$sub_total", "$follower"]}
        #     }},
        #     {"$group": {
        #         "_id": null,
        #         "total_cnt": {"$sum": {"$toInt": 1}},
        #         "total_eng": {"$sum": "$eng_rate"}
        #     }},
        #     {"$project": {
        #         "_id": 0,
        #         "total_eng": {
        #             "$round": [
        #                 {"$divide": ["$total_eng", "$total_cnt"]},
        #                 3
        #             ]}
        #     }},
        #     {"$project": {
        #         "_id": 0,
        #         "latest_10_avg_eng":
        #             {"$multiply": ["$total_eng", 100]}
        #     }}
        # ])
