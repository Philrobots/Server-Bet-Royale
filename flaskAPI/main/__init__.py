from flask import Flask
from flask_cors import CORS
from main.api.GolfApi import GolfApi
from main.api.errors.errors import errors
from flask_mail import Mail, Message

app = Flask(__name__)
cors = CORS(app, resource={r"/*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'betroyale67@gmail.com'
app.config['MAIL_PASSWORD'] = 'plnstkgnfanqcyww'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

API = GolfApi(app, errors=errors)
mail = Mail(app)

if app.config["ENV"] == "production":
    app.config.from_object("config.ProductionConfig")
elif app.config["ENV"] == "testing":
    app.config.from_object("config.TestingConfig")
else:
    app.config.from_object("config.DevelopmentConfig")