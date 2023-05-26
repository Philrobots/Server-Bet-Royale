

from datetime import datetime
from main.domain.exception.SportsGameCompletedException import SportsGameCompletedException
from main.domain.identifiers.DomainId import DomainId
from main.domain.sports_game.bookmakers.BookMakers import BookMakers
from main.domain.sports_game.score.Score import Score


class SportsGame:
    def __init__(self, id: DomainId, external_id: str, team_home: str, team_away: str, game_start: datetime, game_end: datetime, sport: str, league: str, score: Score,
                 completed: bool, book_makers: BookMakers):
        self.id = id
        self.external_id = external_id
        self.team_home = team_home
        self.team_away = team_away
        self.game_start = game_start
        self.game_end = game_end
        self.sport = sport
        self.league = league
        self.score = score
        self.completed = completed
        self.book_makers = book_makers

    def verify_completed_for_bet_creation(self):
        if self.completed:
            raise SportsGameCompletedException

    def is_completed(self) -> bool:
        return self.completed

    def home_wins(self) -> bool:
        return self.score.home_wins()
