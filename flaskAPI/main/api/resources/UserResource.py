from flask import jsonify, request
from main.domain.identifiers.DomainId import DomainId
from main.infra.authentication.TokenDecoder import TokenDecoder
from main.service.UserService import UserService
from flask_restful import Resource


class UserResource(Resource):

    def __init__(self, user_service: UserService, token_decoder: TokenDecoder):
        self.user_service = user_service
        self.token_decoder = token_decoder

    def get(self):
        auth_token = request.headers.get("Authorization", "")
        user_id = DomainId(self.token_decoder.decode_auth_token(auth_token))
        user = self.user_service.get_by_id(user_id)
        response = jsonify({"email": user.email, "username": user.username})
        return response
