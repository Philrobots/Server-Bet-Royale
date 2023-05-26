from main.infra.authentication.TokenDecoder import TokenDecoder
from main.service.UserService import UserService
from flask_restful import Resource


class LeaderboardResource(Resource):

    def __init__(self, user_service: UserService, token_decoder: TokenDecoder):
        self.user_service = user_service
        self.token_decoder = token_decoder

    def get(self):
        return self.user_service.get_leaders()
