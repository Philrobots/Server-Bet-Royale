
from flask_restful import Resource
from main.api.schemas.response.SportsGameResponseSchema import SportsGameResponseSchema

from main.service.SportsGameService import SportsGameService


class SportsGameResource(Resource):

    def __init__(self, sports_game_service:SportsGameService, sports_game_response_schema:SportsGameResponseSchema):
        self.sports_game_service = sports_game_service
        self.sports_game_response_schema = sports_game_response_schema

    def get(self):
        #basket_ball_games = self.sports_game_service.get_basketball_sports_games()
        #hockey_games = self.sports_game_service.get_hockey_sports_games()
        mma_games = self.sports_game_service.get_mma_sports_games()
        baseball_games = self.sports_game_service.get_mlb_sports_games()
        soccer_mls_games = self.sports_game_service.get_mls_sports_games()
        nfl_games = self.sports_game_service.get_nfl_games()
        

        return {
            'basketball': [],
            'hockey': [],
            'mma': [self.sports_game_response_schema.dump(sports_game) for sports_game in mma_games],
            'baseball': [self.sports_game_response_schema.dump(sports_game) for sports_game in baseball_games],
            'soccer_mls': [self.sports_game_response_schema.dump(sports_game) for sports_game in soccer_mls_games],
            'nfl_football': [self.sports_game_response_schema.dump(sports_game) for sports_game in nfl_games]
        }