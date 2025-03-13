from flask import Flask, jsonify, request, Blueprint
from flask_cors import CORS
from random import randint
from config import Config
from models import main_db, general_db
from firebase.firebase_auth import verify_firebase_token
from instagram.routes import *
from youtube.routes import *
from bilibili.routes import *
from music.routes import *
from artist.routes import *
from tiktok.routes import *
from news.routes import *
from twitter.routes import *
from user.routes import *
from campaign.routes import *
from firebase_admin import credentials, auth


app = Flask(__name__)
CORS(app, resources={r'/*': {'origins': '*'}}, supports_credentials=True)

# register blueprint
app.register_blueprint(instagram_api_bp)
app.register_blueprint(youtube_api_bp)
app.register_blueprint(bilibili_api_bp)
app.register_blueprint(music_api_bp)
app.register_blueprint(artist_api_bp)
app.register_blueprint(tiktok_api_bp)
app.register_blueprint(news_api_bp)
app.register_blueprint(twitter_api_bp)
app.register_blueprint(user_api_bp)

#initialize firebase admin SDK
# cred = credentials.Certificate('path/to/your/serviceAccountKey.json')
# firebase_admin.initialize_app(cred)

# add resource endpoint
# Instagram
instagram_api.add_resource(InstagramPost, '/instagram/post')
instagram_api.add_resource(InstagramPostCategory, '/instagram/post/cat')
instagram_api.add_resource(InstagramCategoryPercentage, '/instagram/post/topic-prc')
# YouTube
youtube_api.add_resource(YoutubePost, '/youtube/post')
youtube_api.add_resource(YoutubeUsedTags, '/youtube/tags/most-used')
youtube_api.add_resource(YoutubeEngagedTags, '/youtube/tags/most-engaged')
youtube_api.add_resource(YoutubeComment, '/youtube/comment')
# Bilibili
bilibili_api.add_resource(BilibiliPost, '/bilibili/post')
# Music
music_api.add_resource(SpotifyIndex, '/spotify/index')
music_api.add_resource(MelonFollower, '/melon/follower')
music_api.add_resource(WeeklyMusicCharts, '/weekly/music-charts')
music_api.add_resource(SpotifyTopTrackByCountry, '/spotify/top-track')
music_api.add_resource(SpotifyTopTrackPopularityByRegion, '/spotify/top-track/region')
music_api.add_resource(CircleChartRetailAlbum, '/circle/chart/retail-album')
music_api.add_resource(MusicCenterMusicBroadcast, '/music-broadcast/music-center/chart')
music_api.add_resource(McountdownMusicBroadcast, '/music-broadcast/mcountdown/chart')
music_api.add_resource(ShowChampionMusicBroadcast, '/music-broadcast/show-champion/chart')
music_api.add_resource(TheShowMusicBroadcast, '/music-broadcast/the-show/chart')
music_api.add_resource(InkigayoMusicBroadcast, '/music-broadcast/inkigayo/chart')
#Artist Info
artist_api.add_resource(CampaignPackageDetail, '/campaign')
artist_api.add_resource(ArtistInfo, '/artist/info')
#Trending Artist
artist_api.add_resource(ArtistPopularity, '/trending-artist/rank')
artist_api.add_resource(CalculateDramaScore, '/trending-artist/drama')
# Tiktok
tiktok_api.add_resource(TiktokPost, '/tiktok/post')
# News
news_api.add_resource(TheQooHot, '/theqoo/hot')
# Twitter
twitter_api.add_resource(TwitterIndex, '/twitter/index')
#Campaign



@app.route('/verify-token', methods=['POST'])
def verify_token():
    # Get token from Authorization Header
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({'error': 'Authorization header is missing or invalid'}), 401

    id_token = auth_header.split('Bearer ')[1]  # Get token

    try:
        # Authenticate Firebase ID Token
        decoded_token = auth.verify_id_token(id_token)
        uid = decoded_token['uid']  #get user ID
        email = decoded_token.get('email')  #get user email

        # return success
        return jsonify({
            'message': 'Token is valid',
            'uid': uid,
            'email': email
        }), 200
    except Exception as e:
        # error
        return jsonify({'error': str(e)}), 401


@app.route('/protected-route')
def protected():
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return jsonify({"error": "Unauthorized"}), 401

    token = auth_header.split(" ")[1]
    decoded_token = verify_firebase_token(token)

    if not decoded_token:
        return jsonify({"error": "Invalid token"}), 401

    return jsonify({"message": "Access granted", "user": decoded_token}), 200


@app.route('/', methods=['GET'])
def root():
    text = "Welcome Flask"
    return text


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)