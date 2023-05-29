from flask import jsonify, request
from flask_restful import Resource
from stream_chat import StreamChat


class ChatResource(Resource):

    def __init__(self):
        self.client = StreamChat(
            "5sj7ykpnrmyz", "ad3ak53kz4bueppex6pqehtr69smjwkdm6vap9w7xhg3fxkbsmr2vmuw9t5ehhn5")

    def get(self):
        args = request.args
        user_id = args.get('user_id')
        return self.client.create_token(user_id)
