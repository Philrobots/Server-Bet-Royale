
from flask_restful import Resource
from main.api.schemas.response.SportsGameResponseSchema import SportsGameResponseSchema

from main.service.SportsGameService import SportsGameService


class SportsGameResource(Resource):

    def __init__(self, sports_game_service:SportsGameService, sports_game_response_schema:SportsGameResponseSchema):
        self.sports_game_service = sports_game_service
        self.sports_game_response_schema = sports_game_response_schema

    def get(self):
        basket_ball_games = []
        hockey_games = []
        mma_games = []
        baseball_games = []
        soccer_mls_games = []
        nfl_games = []
        
        all_sports_game = self.sports_game_service.get_active_game()
        
        
        for sport_game in all_sports_game:
            if sport_game.sport == 'americanfootball':
                nfl_games.append(sport_game)
            elif sport_game.sport == 'mma':
                mma_games.append(sport_game)
            elif sport_game.sport == 'baseball':
                baseball_games.append(sport_game)
            elif sport_game.sport == 'soccer':
                soccer_mls_games.append(sport_game)
            elif sport_game.sport == 'icehockey':
                hockey_games.append(sport_game)
            elif sport_game.sport == 'basketball':
                basket_ball_games.append(sport_game)

        return {
            'basketball': [self.sports_game_response_schema.dump(sports_game) for sports_game in basket_ball_games],
            'hockey': [self.sports_game_response_schema.dump(sports_game) for sports_game in hockey_games],
            'mma': [self.sports_game_response_schema.dump(sports_game) for sports_game in mma_games],
            'baseball': [self.sports_game_response_schema.dump(sports_game) for sports_game in baseball_games],
            'soccer_mls': [self.sports_game_response_schema.dump(sports_game) for sports_game in soccer_mls_games],
            'nfl_football': [self.sports_game_response_schema.dump(sports_game) for sports_game in nfl_games[0:6]]
        }