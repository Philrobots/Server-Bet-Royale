import requests
from copy import copy


class OddsApiEngine:
    def __init__(self, api_key):
        self.api_key = api_key

    def get_mls_games_with_odds_live(self) -> list[dict]:
        return self._get_games_with_odds("soccer_usa_mls")

    def get_mls_games_with_scores(self) -> list[dict]:
        return self._get_games_with_score("soccer_usa_mls")

    def get_hockey_games_with_odds_live(self) -> list[dict]:
        return self._get_games_with_odds("icehockey_nhl")

    def get_old_hockey_games_with_scores(self) -> list[dict]:
        return self._get_games_with_score("icehockey_nhl")

    def get_nba_games_with_scores(self) -> list[dict]:
        return self._get_games_with_score("basketball_nba")

    def get_nba_games_with_odds(self) -> list[dict]:
        return self._get_games_with_odds("basketball_nba")

    def get_mlb_games_with_scores(self) -> list[dict]:
        return self._get_games_with_score("baseball_mlb")

    def get_mlb_games_with_odds(self) -> list[dict]:
        return self._get_games_with_odds("baseball_mlb")

    def get_mma_games_with_scores(self) -> list[dict]:
        return self._get_games_with_score("mma_mixed_martial_arts")

    def get_mma_games_with_odds(self) -> list[dict]:
        return self._get_games_with_odds("mma_mixed_martial_arts")

    def get_mls_games_with_scores_and_odds(self) -> list[dict]:
        odds_dict_list = self.get_mls_games_with_odds_live()
        scores_dict_list = self.get_mls_games_with_scores()
        return self._combine_odds_and_scores(odds_dict_list, scores_dict_list)

    def get_mma_games_with_scores_and_odds(self) -> list[dict]:
        odds_dict_list = self.get_mma_games_with_odds()
        scores_dict_list = self.get_mma_games_with_scores()
        return self._combine_odds_and_scores(odds_dict_list, scores_dict_list)

    def get_hockey_games_with_scores_and_odds(self) -> list[dict]:
        odds_dict_list = self.get_hockey_games_with_odds_live()
        scores_dict_list = self.get_old_hockey_games_with_scores()
        return self._combine_odds_and_scores(odds_dict_list, scores_dict_list)

    def get_nba_games_with_scores_and_odds(self) -> list[dict]:
        odds_dict_list = self.get_nba_games_with_odds()
        scores_dict_list = self.get_nba_games_with_scores()
        return self._combine_odds_and_scores(odds_dict_list, scores_dict_list)

    def get_mlb_games_with_scores_and_odds(self) -> list[dict]:
        odds_dict_list = self.get_mlb_games_with_odds()
        scores_dict_list = self.get_mlb_games_with_scores()
        return self._combine_odds_and_scores(odds_dict_list, scores_dict_list)

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
