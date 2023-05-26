from marshmallow import Schema
from main.infra.schemas.field.CurrencyField import CurrencyField


class AddBetterFundsRequestSchema(Schema):
    amount = CurrencyField(required=True)