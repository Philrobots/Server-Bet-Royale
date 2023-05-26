


from ctypes import Array
from main.domain.date.DateTimeHelper import DateTimeHelper
from main.domain.identifiers.DomainId import DomainId
from main.domain.sports_game.SportsGame import SportsGame
from main.domain.sports_game.bookmakers.BookMakersFactory import BookMakersFactory
from main.domain.sports_game.score.Score import Score


class SportsGameFactory:
    def __init__(self, date_time_helper: DateTimeHelper, book_makers_factory: BookMakersFactory):
        self.date_time_helper = date_time_helper
        self.book_makers_factory = book_makers_factory

    def create(self, sports_response) -> SportsGame:
        
        if "completed" not in sports_response:
            sports_response["completed"] = False

        if "bookmakers" in sports_response and sports_response["bookmakers"] != []:
            book_makers = self.book_makers_factory.create(sports_response)
        else:
            book_makers = None
        
        
        if "scores" not in sports_response or sports_response["scores"] is None:
            score = None
        else:
            score = Score(self._find_team_score(sports_response["scores"], sports_response["home_team"]), self._find_team_score(sports_response["scores"], sports_response["away_team"]))

        return SportsGame(DomainId(), sports_response["id"], sports_response["home_team"], sports_response["away_team"], 
                self.date_time_helper.create_datetime_from_iso(sports_response["commence_time"]), None, sports_response["sport_key"].split("_")[0],
                sports_response["sport_title"], score, completed=sports_response["completed"], book_makers=book_makers)

                

    def _find_team_score(self, scores_array:Array[dict], team_name:str) -> int:
        for score in scores_array:
            if score["name"] == team_name:
                return int(score["score"])
