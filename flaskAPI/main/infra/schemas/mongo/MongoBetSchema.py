


from marshmallow import Schema, fields, pre_dump, post_load
from main.domain.bet.Bet import Bet
from main.infra.db.repository.SportsGameRepository import SportsGameRepository

from main.infra.schemas.field.MongoDomainIdField import MongoDomainIdField
from main.infra.schemas.mongo.MongoOddsSchema import MongoOddsSchema
from main.infra.schemas.mongo.MongoBetAmountSchema import MongoBetAmountSchema
from copy import copy


class MongoBetSchema(Schema):
    def __init__(self, sports_game_repo:SportsGameRepository):
        super().__init__()
        self.sports_game_repo = sports_game_repo

    id = MongoDomainIdField(data_key="_id", required=True)
    odds = fields.Nested(MongoOddsSchema, required=True)
    sports_game = MongoDomainIdField(data_key="sports_game_id", required=True)
    bet_amounts_home = fields.List(fields.Nested(MongoBetAmountSchema), required=True)
    bet_amounts_away = fields.List(fields.Nested(MongoBetAmountSchema), required=True)
    is_completed = fields.Bool(required=True)
    is_home_bet = fields.Bool(required=True)
    is_accepted = fields.Bool(required=True)
    owner_id = MongoDomainIdField(required=True)
    
    @post_load
    def fetch_sports_game_and_build_bet(self, data, **kwargs):
        sports_game = self.sports_game_repo.get_by_id(data["sports_game"])

        data["sports_game"] = sports_game
        return Bet(**data)
    
    @pre_dump
    def pre_dump_sports_game(self, data, **kwargs):
        data_copy = copy(data)
        data_copy.sports_game = data.sports_game.id
        return data_copy