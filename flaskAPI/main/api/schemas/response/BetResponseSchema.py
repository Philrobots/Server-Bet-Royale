from main.domain.exception.NoOpponentIdException import NoOpponentIdException
from main.domain.identifiers.DomainId import DomainId
from main.infra.db.repository.UserAuthRepository import UserAuthRepository
from marshmallow import Schema, fields, pre_dump, post_load
from main.api.schemas.field.IdField import IdField
from main.api.schemas.response.BetAmountResponseSchema import BetAmountResponseSchema
from main.api.schemas.response.SportsGameResponseSchema import SportsGameResponseSchema
from copy import copy
from main.infra.schemas.mongo.MongoOddsSchema import MongoOddsSchema


class BetResponseSchema(Schema):
    
    def __init__(self, user_auth_repository: UserAuthRepository):
        super().__init__()
        self.user_auth_repository = user_auth_repository
        
    id = IdField(required=True)
    odds = fields.Nested(MongoOddsSchema, required=True)
    sports_game = fields.Nested(SportsGameResponseSchema, required=True)
    bet_amounts_home = fields.List(fields.Nested(BetAmountResponseSchema), required=True)
    bet_amounts_away = fields.List(fields.Nested(BetAmountResponseSchema), required=True)
    is_completed = fields.Bool(required=True)
    is_home_bet = fields.Bool(required=True)
    is_accepted = fields.Bool(required=True)
    owner_id = IdField(required=True)
    owner_username = fields.String(required=True)
    opponent_username = fields.String(required=True)
    is_owner = fields.Bool(required=False)
    


    def get_opponent_username(self, data_copy):
        try:
            opponent_id = data_copy.get_opponent_id()
            user = self.user_auth_repository.get_by_id(opponent_id)
            return user.username
        except NoOpponentIdException:
            return "No opponent"

    def get_owner_username(self, data_copy):
        user = self.user_auth_repository.get_by_id(data_copy.owner_id)
        return user.username
        

    @pre_dump
    def pre_dump_sports_game(self, data, **kwargs):
        data_copy = copy(data)
        data_copy.opponent_username = self.get_opponent_username(data_copy)
        data_copy.owner_username = self.get_owner_username(data_copy)
        return data_copy
    