from flask import Flask
from routes.melon_route import *
from routes.spotify_route import *
from routes.youtube_route import *
from routes.instagram_route import *
from routes.tiktok_route import *
from routes.user_route import *
from routes.trending_artist_route import *
from routes.artist_route import *
from routes.bilibili_route import *
from routes.tenant_route import *
from db_connect import connect_db
from config import  Config
from flask_cors import CORS
import firebase_admin
from firebase_admin import credentials


def create_app():
    app = Flask(__name__)

    CORS(app, resources={r'/*': {'origins': '*'}}, supports_credentials=True)

    # app.config.from_object(Config)
    # Initialize Firebase Admin SDK
    cred = credentials.Certificate('./firebase/venv/serviceAccountKey.json')
    firebase_admin.initialize_app(cred)

    # register blueprints
    app.register_blueprint(melon_bp, url_prefix="/api/melon")
    app.register_blueprint(spotify_bp, url_prefix="/api/spotify")
    app.register_blueprint(youtube_bp, url_prefix="/api/youtube")
    app.register_blueprint(instagram_bp, url_prefix="/api/instagram")
    app.register_blueprint(tiktok_bp, url_prefix="/api/tiktok")
    app.register_blueprint(user_bp, url_prefix="/api/user")
    app.register_blueprint(trending_artist_bp, url_prefix="/api/trending-artist")
    app.register_blueprint(artist_bp, url_prefix="/api/artist")
    app.register_blueprint(bilibili_bp, url_prefix="/api/bilibili")
    app.register_blueprint(tenant_bp, url_prefix="/api/tenant")

    # init DB
    try:
        print("Initializing DB connection...")
        connect_db()
        print("DB initialized.")
    except Exception as e:
        print(f"Database connection failed: {e}", flush=True)

    return app
