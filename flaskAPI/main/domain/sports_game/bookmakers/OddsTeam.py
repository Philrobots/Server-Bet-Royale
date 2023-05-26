class OddsTeam:
    
    def __init__(self, odds: float, team: str, is_home_team: bool) -> None:
        self.odds = odds
        self.team = team
        self.is_home_team = is_home_team
        