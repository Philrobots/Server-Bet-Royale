class SportsKey:

    def __init__(self) -> None:
        self.american_football_nfl = 'americanfootball_nfl'
        self.cfl_football = 'americanfootball_cfl'
        self.american_nfl_preseason = 'americanfootball_nfl_preseason'
        self.us_college_football = 'americanfootball_ncaaf'
        self.baseball_mlb = 'baseball_mlb'
        self.mma = 'mma_mixed_martial_arts'
        self.england_premier_league = 'soccer_epl'
        self.france_league_one = 'soccer_france_ligue_one'
        self.spain_la_liga = 'soccer_spain_la_liga'
        self.ice_hockey_nhl = 'icehockey_nhl'
        self.soccer_mls = 'soccer_usa_mls'
        self.basketball_nba = 'basketball_nba'

    # Change this depending on sports you want to get
    def get_active_sports(self) -> list[str]:
        return [
            self.american_football_nfl,
            self.american_nfl_preseason,
            self.us_college_football,
            self.baseball_mlb,
            self.england_premier_league,
            self.spain_la_liga,
            self.cfl_football
        ]
