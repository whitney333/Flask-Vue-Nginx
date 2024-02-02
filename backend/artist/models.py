import os
import pymongo
from flask import Flask
from werkzeug.security import generate_password_hash, check_password_hash
import hashlib


app = Flask(__name__)
# app.config.from_object(Config)

cloud_client = pymongo.MongoClient(os.environ["DB_HOST"],
                                   username=os.environ["DB_USERNAME"],
                                   password=os.environ["DB_PASSWORD"])
main_db = cloud_client["t024"]
general_db = cloud_client["general"]
news_db = cloud_client["news"]
campaign_db = cloud_client["campaign_package"]