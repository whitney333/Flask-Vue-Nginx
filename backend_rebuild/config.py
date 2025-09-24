import os

class Config(object):
    os.environ["DB_HOST"] = "mongodb://18.162.155.254:27017/"
    os.environ["DB_USERNAME"] = "admin"
    os.environ["DB_PASSWORD"] = "demo1008"
    os.environ["DB_NAME"] = "general"
