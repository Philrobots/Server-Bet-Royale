
from marshmallow import Schema, fields

from main.api.schemas.field.IdField import IdField
from main.infra.schemas.field.CurrencyField import CurrencyField


class CreateBetRequestSchema(Schema):
    sports_game_id = IdField(required=True)
    bet_amount = CurrencyField(required=True)
    odds = fields.Float(required=True)
    is_home_bet = fields.Bool(required=True)