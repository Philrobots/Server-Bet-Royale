from main.infra.schemas.mongo.MongoBookMakerSchema import MongoBookMakerSchema
from marshmallow import Schema, fields
from main.api.schemas.field.IdField import IdField
from main.infra.schemas.field.ScoreField import ScoreField


class SportsGameResponseSchema(Schema):
    id = IdField(required=True)
    external_id = fields.String(required=True)
    team_home = fields.String(required=True)
    team_away = fields.String(required=True)
    game_start = fields.AwareDateTime(required=True)
    game_end = fields.AwareDateTime(required=True, allow_none=True)
    sport = fields.String(required=True)
    league = fields.String(required=True)
    score = ScoreField(required=True, allow_none=True)
    completed = fields.Bool(required=True)
    book_makers = fields.Nested(MongoBookMakerSchema, required=True)