
from marshmallow import Schema, fields

from main.infra.schemas.field.CurrencyField import CurrencyField


class GiftResponseSchema(Schema):
    can_receive = fields.Bool(required=True)
    price = CurrencyField(required=True)