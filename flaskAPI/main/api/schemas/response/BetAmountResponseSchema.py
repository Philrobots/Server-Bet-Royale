
from marshmallow import Schema, fields

from main.api.schemas.field.IdField import IdField
from main.infra.schemas.field.CurrencyField import CurrencyField


class BetAmountResponseSchema(Schema):

    id = IdField(required=True)
    is_author = fields.Bool(required=True)
    better_id = IdField(required=True)
    amount = CurrencyField(required=True)