from main.infra.schemas.mongo.MongoBookMakerSchema import MongoBookMakerSchema
from marshmallow import Schema, fields, post_load
from main.domain.sports_game.SportsGame import SportsGame
from main.infra.schemas.field.MongoDomainIdField import MongoDomainIdField
from main.infra.schemas.field.ScoreField import ScoreField


class MongoSportsGameSchema(Schema):
    id = MongoDomainIdField(data_key="_id", required=True)
    external_id = fields.String(required=True)
    team_home = fields.String(required=True)
    team_away = fields.String(required=True)
    game_start = fields.AwareDateTime(required=True)
    game_end = fields.AwareDateTime(required=True, allow_none=True)
    sport = fields.String(required=True)
    league = fields.String(required=True)
    score = ScoreField(required=True, allow_none=True)
    completed = fields.Bool(required=True)
    book_makers = fields.Nested(MongoBookMakerSchema, required=True, allow_none=True)

    @post_load()
    def create_sports_game(self, data, **kwargs):
        return SportsGame(**data)