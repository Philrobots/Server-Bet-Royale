
from marshmallow import Schema, fields

from main.api.schemas.field.IdField import IdField
from main.infra.schemas.field.CurrencyField import CurrencyField


class GiftResponseSchema(Schema):
    user_id = IdField(required=True)
    can_receive = fields.Bool(required=True)
    price = CurrencyField(required=True)