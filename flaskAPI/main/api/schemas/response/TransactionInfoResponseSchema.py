


from marshmallow import Schema, fields

from main.api.schemas.field.IdField import IdField
from main.api.schemas.response.TruncatedSportsGameResponseSchema import TruncatedSportsGameResponseSchema
from main.domain.transaction.TransactionType import TransactionType
from main.infra.schemas.field.CurrencyField import CurrencyField


class TransactionInfoResponseSchema(Schema):
    transaction_id = IdField(required=True)
    amount = CurrencyField(required=True)
    transaction_type = fields.Enum(TransactionType, required=True)
    date_created = fields.DateTime(required=True)
    sports_game = fields.Nested(TruncatedSportsGameResponseSchema, required=True)
    current_balance = CurrencyField(required=True)