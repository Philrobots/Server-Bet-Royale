from marshmallow import Schema, fields
from main.api.schemas.field.IdField import IdField
from main.infra.schemas.field.ScoreField import ScoreField


class TruncatedSportsGameResponseSchema(Schema):
    id = IdField(required=True)
    team_home = fields.String(required=True)
    team_away = fields.String(required=True)
    game_start = fields.AwareDateTime(required=True)
    game_end = fields.AwareDateTime(required=True, allow_none=True)
    sport = fields.String(required=True)
    league = fields.String(required=True)
    score = ScoreField(required=True, allow_none=True)
    completed = fields.Bool(required=True)