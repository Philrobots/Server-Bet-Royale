from flask import request, jsonify
from flask_restful import Resource
from main.service.UserService import UserService


class LoginResource(Resource):

    def __init__(self, user_service: UserService):
        self.user_service = user_service

    def post(self):
        username = request.json.get("username", "")
        password = request.json.get("password", "")
        token = self.user_service.login(username, password)
        return jsonify({"token": token.to_string()})
