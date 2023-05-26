from main.domain.sports_game.bookmakers.BookMakers import BookMakers
from main.domain.sports_game.bookmakers.OddsTeam import OddsTeam


class BookMakersFactory:
    

    def create(self, sports_response:dict) -> BookMakers:
        outcomes = self._get_path_to_outcomes(sports_response)
        
        if self._is_first_outcomes_home_team(sports_response, outcomes):
            home_team_odds = OddsTeam(odds=outcomes[0]["price"], team=outcomes[0]["name"], is_home_team=True)
            away_team_odds = OddsTeam(odds=outcomes[1]["price"], team=outcomes[1]["name"], is_home_team=False)
            return BookMakers([home_team_odds, away_team_odds])
        else:
            home_team_odds = OddsTeam(odds=outcomes[1]["price"], team=outcomes[1]["name"], is_home_team=True)
            away_team_odds = OddsTeam(odds=outcomes[0]["price"], team=outcomes[0]["name"], is_home_team=False)
            return BookMakers(winner_odds=[home_team_odds, away_team_odds])

    def _is_first_outcomes_home_team(self, sports_response, outcomes):
        return outcomes[0]["name"] == sports_response["home_team"]

    def _get_path_to_outcomes(self, sports_response):
        return sports_response["bookmakers"][0]["markets"][0]["outcomes"]