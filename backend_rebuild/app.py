from flask import Flask
from routes.melon_route import *
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
    app.register_blueprint(melon_bp, url_prefix="/api")


    return app
