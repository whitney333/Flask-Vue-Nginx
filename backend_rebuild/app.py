import os
from dotenv import load_dotenv

environment = os.getenv("FLASK_ENV", "development")  # default to 'dev'
env_file = f".env.{environment}"
if os.path.exists(env_file):
    load_dotenv(dotenv_path=env_file)

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
from routes.campaign_route import *
from routes.admin_route import *
from routes.stripe_route import *
from db_connect import connect_db
from flask_cors import CORS
import firebase_admin
from firebase_admin import credentials
import stripe

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
if stripe.api_key is None:
    raise ValueError("Stripe API key not found in environment")

import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s'
)
logger = logging.getLogger(__name__)

def create_app():
    app = Flask(__name__)

    cors_origins_env = os.getenv("CORS_ALLOWED_ORIGINS", "").strip()
    origins = [o.strip() for o in cors_origins_env.split(",") if o.strip()]
    if not origins:
        frontend_url = os.getenv("FRONTEND_URL", "").strip()
        if frontend_url:
            origins = [frontend_url]

    if origins:
        # Never allow credentials with wildcard origins.
        supports_credentials = "*" not in origins
        CORS(app, resources={r"/*": {"origins": origins}}, supports_credentials=supports_credentials)
    else:
        logger.warning("CORS_ALLOWED_ORIGINS/FRONTEND_URL not set; CORS is disabled.")

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
    app.register_blueprint(campaign_bp, url_prefix="/api/campaign")
    app.register_blueprint(admin_bp, url_prefix="/api/admin")
    app.register_blueprint(stripe_bp, url_prefix="/api/stripe")

    # init DB
    try:
        logger.info("Initializing DB connection...")
        connect_db()
        logger.info("DB initialized.")
    except Exception as e:
        logger.error(f"Database connection failed: {e}")

    return app
