
from flask_restful import Resource
from main.api.resources.SportsKey import SportsKey
from main.api.resources.response.SportsGameResponse import SportsGameResponse
from main.api.schemas.response.SportsGameResponseSchema import SportsGameResponseSchema

from main.service.SportsGameService import SportsGameService


class SportsGameResource(Resource):

    def __init__(self, sports_game_service:SportsGameService, sports_game_response_schema:SportsGameResponseSchema, sports_key: SportsKey):
        self.sports_game_service = sports_game_service
        self.sports_game_response_schema = sports_game_response_schema
        self.sports_key = sports_key

    def get(self) -> dict:
        all_sports_game = self.sports_game_service.get_active_game()
        sports_game_response = SportsGameResponse(all_sports_game=all_sports_game, 
                                                 sports_game_response_schema=self.sports_game_response_schema)
        return sports_game_response.get_games()