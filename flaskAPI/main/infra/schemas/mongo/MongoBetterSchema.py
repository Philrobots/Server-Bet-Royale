from marshmallow import Schema, fields, post_load
from main.domain.bet.Better import Better
from main.infra.schemas.field.CurrencyField import CurrencyField
from main.infra.schemas.field.MongoDomainIdField import MongoDomainIdField


class MongoBetterSchema(Schema):
    def __init__(self, transaction_handler):
        super().__init__()
        self.transaction_handler = transaction_handler

    user_id = MongoDomainIdField(data_key="_id", required=True)
    birth_date = fields.DateTime(required=True)
    bank_balance = CurrencyField(required=True)
    created_bet_ids = fields.List(MongoDomainIdField, required=True)
    accepted_bet_ids = fields.List(MongoDomainIdField, required=True)

    @post_load()
    def create_better(self, data, **kwargs):
        return Better(**data, transaction_handler=self.transaction_handler)
