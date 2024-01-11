import os
import pymongo
from flask import Flask
from werkzeug.security import generate_password_hash, check_password_hash
import hashlib


app = Flask(__name__)

cloud_client = pymongo.MongoClient(os.environ["DB_HOST"],
                                   username=os.environ["DB_USERNAME"],
                                   password=os.environ["DB_PASSWORD"])
main_db = cloud_client["t024"]
music_db = cloud_client["music"]
general_db = cloud_client["general"]
yt_db = cloud_client["youtube"]
news_db = cloud_client["news"]
