
from main.domain.sports_game.score.Score import Score
from marshmallow.fields import Field

class ScoreField(Field):

    def _deserialize(self, score_dict: dict, *args, **kwargs):
        return Score(score_dict["score_home"], score_dict["score_away"])

    def _serialize(self, value: Score, *args, **kwargs):
        return value.serialize() if value is not None else value
