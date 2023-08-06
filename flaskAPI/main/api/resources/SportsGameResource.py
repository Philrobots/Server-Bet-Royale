
from flask_restful import Resource
from main.api.resources.SportsKey import SportsKey
from main.api.schemas.response.SportsGameResponseSchema import SportsGameResponseSchema

from main.service.SportsGameService import SportsGameService


class SportsGameResource(Resource):

    def __init__(self, sports_game_service:SportsGameService, sports_game_response_schema:SportsGameResponseSchema, sports_key: SportsKey):
        self.sports_game_service = sports_game_service
        self.sports_game_response_schema = sports_game_response_schema
        self.sports_key = sports_key

    def get(self) -> dict:
        basket_ball_games = []
        hockey_games = []
        mma_games = []
        baseball_games = []
        soccer_mls_games = []
        nfl_games = []
        us_college_football = []
        england_premier_league = []
        spain_la_liga = []
        nfl_preseason = []
        
        all_sports_game = self.sports_game_service.get_active_game()
        
        for sport_game in all_sports_game:
            if sport_game.sport == self.sports_key.american_nfl_preseason:
                nfl_preseason.append(sport_game)
            if sport_game.sport == self.sports_key.american_football_nfl:
                nfl_games.append(sport_game)
            elif sport_game.sport == self.sports_key.mma:
                mma_games.append(sport_game)
            elif sport_game.sport == self.sports_key.baseball_mlb:
                baseball_games.append(sport_game)
            elif sport_game.sport == self.sports_key.soccer_mls:
                soccer_mls_games.append(sport_game)
            elif sport_game.sport == self.sports_key.ice_hockey_nhl:
                hockey_games.append(sport_game)
            elif sport_game.sport == self.sports_key.basketball_nba:
                basket_ball_games.append(sport_game)
            elif sport_game.sport == self.sports_key.us_college_football:
                us_college_football.append(sport_game)
            elif sport_game.sport == self.sports_key.england_premier_league: 
                england_premier_league.append(sport_game)   
            elif sport_game.sport == self.sports_key.spain_la_liga:
                spain_la_liga.append(sport_game)

        return {
            'nfl_preseason': [self.sports_game_response_schema.dump(sports_game) for sports_game in nfl_preseason],
            'basketball': [self.sports_game_response_schema.dump(sports_game) for sports_game in basket_ball_games],
            'hockey': [self.sports_game_response_schema.dump(sports_game) for sports_game in hockey_games],
            'mma': [self.sports_game_response_schema.dump(sports_game) for sports_game in mma_games],
            'baseball': [self.sports_game_response_schema.dump(sports_game) for sports_game in baseball_games],
            'soccer_mls': [self.sports_game_response_schema.dump(sports_game) for sports_game in soccer_mls_games],
            'nfl_football': [self.sports_game_response_schema.dump(sports_game) for sports_game in nfl_games[0:8]],
            'us_college_football': [self.sports_game_response_schema.dump(sports_game) for sports_game in us_college_football],
            'england_premier_league': [self.sports_game_response_schema.dump(sports_game) for sports_game in england_premier_league],
            'spain_la_liga': [self.sports_game_response_schema.dump(sports_game) for sports_game in spain_la_liga]
        }