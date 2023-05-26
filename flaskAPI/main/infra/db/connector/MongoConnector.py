from os import environ as env

from pymongo import MongoClient


class MongoConnector(MongoClient):

    def __init__(self):
        super().__init__(env['MONGODB_CONNECTION_STRING'], serverSelectionTimeoutMS=10000)
