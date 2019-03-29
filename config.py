import os
import sys
import json
import datetime

from logger import logger
from bson.objectid import ObjectId

ROOT_PATH = os.path.dirname(os.path.realpath(__file__))
os.environ.update({'ROOT_PATH': ROOT_PATH})


class Config(object):

    SECRET_KEY = os.environ.get('SECRET_KEY') or 'always-trust-in-yourself'

    LOG = logger.get_root_logger(os.environ.get(
        'ROOT_LOGGER', 'root'), filename=os.path.join(ROOT_PATH, 'output.log'))

    PORT = os.environ.get('PORT')

    SQLALCHEMY_DATABASE_URI = os.environ.get('SQL_DATABASE_URL') or \
        'sqlite:///' + os.path.join(ROOT_PATH, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MONGO_URI = os.environ.get('MONGO_DATABASE_URL') or \
        'mongodb://localhost:27017/tembici'


class JSONEncoder(json.JSONEncoder):
    ''' extend json-encoder class'''

    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        if isinstance(o, datetime.datetime):
            return str(o)
        return json.JSONEncoder.default(self, o)
