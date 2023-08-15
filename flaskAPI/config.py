import os

class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.getenv("SECRET_KEY")
    ADMIN_KEY = "Nq[nn#/uIT$AVYS`{H;:V=,OM[LR8sr!^?B<}u[5jy-]K+^nTLf87Fmil[cMq?k"
    ODDS_API_KEY = os.getenv("ODDS_API_KEY")
    PAYPAL_API_URL = os.getenv("PAYPAL_API_URL")
    PAYPAL_CLIENT_ID = os.getenv("PAYPAL_CLIENT_ID")
    PAYPAL_SECRET = os.getenv("PAYPAL_SECRET")
    CLIENT_DOMAIN = os.getenv("CLIENT_DOMAIN")

class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    DEBUG = True
    SECRET_KEY = "cestunsecret"


class TestingConfig(Config):
    TESTING = True
