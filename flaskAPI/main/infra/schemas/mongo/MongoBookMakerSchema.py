from main.domain.sports_game.bookmakers.BookMakers import BookMakers
from main.infra.schemas.mongo.MongoWinningOddsSchema import MongoWinningOddsSchema
from marshmallow import Schema, fields, post_load


class MongoBookMakerSchema(Schema):
    winner_odds = fields.List(fields.Nested(MongoWinningOddsSchema), required=True)

    @post_load()
    def create_book_makers(self, data, **kwargs):
        return BookMakers(**data)