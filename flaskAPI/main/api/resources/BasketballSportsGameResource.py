
from flask_restful import Resource
from main.api.schemas.response.SportsGameResponseSchema import SportsGameResponseSchema

from main.service.SportsGameService import SportsGameService


class BasketballSportsGameResource(Resource):

    def __init__(self, sports_game_service:SportsGameService, sports_game_response_schema:SportsGameResponseSchema):
        self.sports_game_service = sports_game_service
        self.sports_game_response_schema = sports_game_response_schema

    def get(self):
        sports_games = self.sports_game_service.get_basketball_sports_games()

        return [self.sports_game_response_schema.dump(sports_game) for sports_game in sports_games]