

from typing import List
from main.domain.sports_game.SportsGame import SportsGame
from main.infra.db.repository.SportsGameRepository import SportsGameRepository


class SportsGameService:
    def __init__(self, sports_game_repo : SportsGameRepository):
        self.sports_game_repo = sports_game_repo

    def get_hockey_sports_games(self) -> List[SportsGame]:
        return self.sports_game_repo.get_hockey_games()

    def get_basketball_sports_games(self) -> List[SportsGame]:
        return self.sports_game_repo.get_basketball_games()

    def get_mlb_sports_games(self) -> List[SportsGame]:
        return self.sports_game_repo.get_mlb_games()

    def get_mma_sports_games(self) -> List[SportsGame]:
        return self.sports_game_repo.get_mma_games()