import os

class Config(object):
    os.environ["DB_HOST"] = "mongodb://43.198.77.59:27017/"
    os.environ["DB_USERNAME"] = "admin"
    os.environ["DB_PASSWORD"] = "demo1008"
    os.environ["DB_NAME"] = "general"
