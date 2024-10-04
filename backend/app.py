from flask import Flask, jsonify, request, Blueprint
from flask_cors import CORS
from random import randint
from config import Config
from models import main_db, general_db
from instagram.routes import *
from youtube.routes import *
from bilibili.routes import *
from music.routes import *
from artist.routes import *
from tiktok.routes import *
from news.routes import *
from twitter.routes import *


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

# Tiktok
tiktok_api.add_resource(TiktokPost, '/tiktok/post')
# News
news_api.add_resource(TheQooHot, '/theqoo/hot')
# Twitter
twitter_api.add_resource(TwitterIndex, '/twitter/index')


@app.route('/', methods=['GET'])
def root():
    text = "Welcome Flask"
    return text

@app.route('/rand', methods=['GET'])
def get_rand():
    response = {
        'randomNum': randint(1,100)
    }
    return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)