from flask import Flask
from flask_cors import CORS
from main.api.GolfApi import GolfApi
from main.api.errors.errors import errors

app = Flask(__name__)
cors = CORS(app, resource={r"/*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'

API = GolfApi(app, errors=errors)

if app.config["ENV"] == "production":
    app.config.from_object("config.ProductionConfig")
elif app.config["ENV"] == "testing":
    app.config.from_object("config.TestingConfig")
else:
    app.config.from_object("config.DevelopmentConfig")