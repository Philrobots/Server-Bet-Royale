
from main.domain.bet.BetAmount import BetAmount
from marshmallow import Schema, fields, post_load
from main.infra.schemas.field.CurrencyField import CurrencyField

from main.infra.schemas.field.MongoDomainIdField import MongoDomainIdField


class MongoBetAmountSchema(Schema):

    id = MongoDomainIdField(data_key="_id", required=True)
    is_author = fields.Bool(required=True)
    better_id = MongoDomainIdField(required=True)
    amount = CurrencyField(required=True)

    @post_load
    def create_bet_amount(self, data, **kwargs):
        return BetAmount(**data)

