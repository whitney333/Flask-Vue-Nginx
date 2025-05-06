from flask import Flask
from routes.melon_route import *
from routes.spotify_route import *
from routes.youtube_route import *
from routes.instagram_route import *
from routes.tiktok_route import *
from routes.user_route import *
from routes.trending_artist_route import *
from config import Config
from mongoengine import *


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # connect database on startup
    connect(
        db='general',
        username='admin',
        password='demo1008',
        authentication_source='admin',
        host="18.162.155.254:27017"
    )

    # register blueprints
    app.register_blueprint(melon_bp, url_prefix="/api/melon")
    app.register_blueprint(spotify_bp, url_prefix="/api/spotify")
    app.register_blueprint(youtube_bp, url_prefix="/api/youtube")
    app.register_blueprint(instagram_bp, url_prefix="/api/instagram")
    app.register_blueprint(tiktok_bp, url_prefix="/api/tiktok")
    app.register_blueprint(user_bp, url_prefix="/api/user")
    app.register_blueprint(trending_artist_bp, url_prefix="/api/trending-artist")

    return app
