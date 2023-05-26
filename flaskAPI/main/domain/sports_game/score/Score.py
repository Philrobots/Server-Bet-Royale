

class Score:
    def __init__(self, score_home: int, score_away: int):
        self.score_home = score_home
        self.score_away = score_away

    def serialize(self):
        return {
            "score_home": self.score_home,
            "score_away": self.score_away
        }
    
    def home_wins(self):
        return self.score_home > self.score_away