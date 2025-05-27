from flask import Flask
from routes.melon_route import *
from routes.spotify_route import *
from routes.youtube_route import *
from routes.instagram_route import *
from routes.tiktok_route import *
from routes.user_route import *
from routes.trending_artist_route import *
from config import Config
import os
import pathlib
from sshtunnel import SSHTunnelForwarder
from dotenv import load_dotenv
from mongoengine import *


def init_db(app):
    load_dotenv(dotenv_path='.env')

    # Create the tunnel
    server = SSHTunnelForwarder(
        (os.getenv(key='EC2_URL'), 22),
        ssh_username='ec2-user',
        ssh_pkey=os.fspath(pathlib.Path(__file__).parent / 'MongoDB.pem'),
        remote_bind_address=(os.getenv(key='DB_URI'), 27017),
        local_bind_address=('127.0.0.1', 27017)
    )
    # Start the tunnel
    server.start()

    # mongoengine connect db
    connect(
        port=27017,
        db='general',
        username=os.getenv(key='DB_USER'),
        password=os.getenv(key='DB_PASS'),
        authMechanism="SCRAM-SHA-1",
        tlsAllowInvalidHostnames=True,
        tls=True,
        tlsCAFile=os.fspath(pathlib.Path(__file__).parent / 'global-bundle.pem'),
        timeoutMS=10000,
        directConnection=True
    )

    print("db connected")

    # server.stop()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # connect database on startup
    # connect(
    #     db='general',
    #     username='admin',
    #     password='demo1008',
    #     authentication_source='admin',
    #     host="18.162.155.254:27017"
    # )
    # MONGODB_CONNECTION = "mongodb://whitneyliao:db_auth#1330@mishkan-db-1.cluster-ccxgvyhgfzay.ap-east-1.docdb.amazonaws.com:27017/?tls=true&tlsCAFile=global-bundle.pem&replicaSet=rs0&readPreference=secondaryPreferred&retryWrites=false"

    ### Init DB ###
    init_db(app)
    # db = client.general
    # x = db.artists.find({})
    # print([i for i in x])

    # register blueprints
    app.register_blueprint(melon_bp, url_prefix="/api/melon")
    app.register_blueprint(spotify_bp, url_prefix="/api/spotify")
    app.register_blueprint(youtube_bp, url_prefix="/api/youtube")
    app.register_blueprint(instagram_bp, url_prefix="/api/instagram")
    app.register_blueprint(tiktok_bp, url_prefix="/api/tiktok")
    app.register_blueprint(user_bp, url_prefix="/api/user")
    app.register_blueprint(trending_artist_bp, url_prefix="/api/trending-artist")

    return app
