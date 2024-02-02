import datetime
import os


class Config(object):
    os.environ["DB_HOST"] = "mongodb://43.198.78.239:27017/"
    os.environ["DB_USERNAME"] = "admin"
    os.environ["DB_PASSWORD"] = "demo1008"
    os.environ["AWS_ACCESS_KEY"] = "AKIAWCQFEI4JBUP6LVBH"
    os.environ["AWS_SECRET_KEY"] = "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"
    os.environ["S3_BUCKET_NAME"] = "sslpopo"

    os.environ.get("AWS_ACCESS_KEY")
    os.environ.get("AWS_SECRET_KEY")
    os.environ.get("S3_BUCKET_NAME")
    os.environ.get("DB_HOST")
    os.environ.get("DB_USERNAME")
    os.environ.get("DB_PASSWORD")