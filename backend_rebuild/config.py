import os

class Config(object):
    # os.environ["DB_HOST"] = "mongodb://18.162.155.254:27017/"
    # os.environ["DB_USERNAME"] = "admin"
    # os.environ["DB_PASSWORD"] = "demo1008"
    # os.environ["DB_NAME"] = "general"
    STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY")
    # Price ID for monthly & yearly
    STRIPE_PRICE_MONTHLY = os.getenv("STRIPE_PRICE_MONTHLY")
    STRIPE_PRICE_YEARLY = os.getenv("STRIPE_PRICE_YEARLY")
    # the page which will be redirected to when client paid successfully
    FRONTEND_URL = os.getenv("FRONTEND_URL")
