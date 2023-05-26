from main.domain.sports_game.bookmakers.OddsTeam import OddsTeam


class BookMakers:
    
    def __init__(self, winner_odds: list[OddsTeam]) -> None:
        self.winner_odds = winner_odds