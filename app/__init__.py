
from config import Config, JSONEncoder
from flask import Flask
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt

app = Flask(__name__)

app.config.from_object(Config)

app.json_encoder = JSONEncoder

app.mongo = PyMongo(app)

app.flask_bcrypt = Bcrypt(app)

from app import routes



