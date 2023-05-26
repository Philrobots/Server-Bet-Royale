from flask import jsonify, request
from main.service import UserService
from flask_restful import Resource


class RegisterResource(Resource):

    def __init__(self, user_service: UserService):
        self.user_service = user_service

    def post(self):
        username = request.json.get("username", "")
        password = request.json.get("password", "")
        email = request.json.get("email", "")
        birth_date = request.json.get("birthdate", "")
        token = self.user_service.register(username, password, email, birth_date)
        response = jsonify({"token": token.to_string()})
        response.status_code = 201
        return response
