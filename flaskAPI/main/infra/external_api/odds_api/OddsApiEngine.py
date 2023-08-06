import requests
from copy import copy
from main.api.resources.SportsKey import SportsKey


class OddsApiEngine:
    
    def __init__(self, api_key, sports_key: SportsKey):
        self.api_key = api_key
        self.sports_key = sports_key
        
        
    def get_sports_games_with_odds_live(self, sport_key: str) -> list[dict]:
        return self._get_games_with_odds(sports_key=sport_key)

    def get_sports_games_with_scores(self, sport_key: str) -> list[dict]:
        return self._get_games_with_score(sports_key=sport_key)
    
    def get_sports_game_with_odds_and_scores(self, sport_key: str) -> list[dict]:
        sports_game_with_odds = self.get_sports_games_with_odds_live(sport_key)
        sports_game_with_score = self.get_sports_games_with_scores(sport_key)
        return self._combine_odds_and_scores(sports_game_with_odds, sports_game_with_score)

    def _combine_odds_and_scores(self, odds_dict_list, scores_dict_list):
        output = copy(scores_dict_list)
        for scores_dict in scores_dict_list:
            game_id = scores_dict["id"]
            first_or_default_odds = next(
                (item for item in odds_dict_list if item["id"] == game_id), None)
            first_or_default_output = next(
                (item for item in output if item["id"] == game_id), None)
            if first_or_default_odds is not None and first_or_default_output is not None:
                first_or_default_output["bookmakers"] = first_or_default_odds["bookmakers"]

        return output

    def _get_games_with_score(self, sports_key):
        return requests.get('https://api.the-odds-api.com/v4/sports/' + sports_key + '/scores', params={
            'api_key': self.api_key,
            'daysFrom': 1
        }).json()

    def _get_games_with_odds(self, sports_key):
        return requests.get('https://api.the-odds-api.com/v4/sports/' + sports_key + '/odds', params={
            'api_key': self.api_key,
            'oddsFormat': 'decimal',
            'regions': 'us',
            "markets": "h2h",
            "bookmakers": "barstool,fanduel,foxbet"
        }).json()
