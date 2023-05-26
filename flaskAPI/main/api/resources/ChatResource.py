from flask import jsonify, request
from flask_restful import Resource
from stream_chat import StreamChat


class ChatResource(Resource):
    
    def __init__(self):
        self.client = StreamChat("4vk9qckeeggf", "9j3e4zfnpn4tttmbegcxvcy7gf8fxeqq969vkgwf4sy8tmyecavym6mwgtqmcz93")

    def get(self):
        args = request.args
        user_id = args.get('user_id')
        return self.client.create_token(user_id)
