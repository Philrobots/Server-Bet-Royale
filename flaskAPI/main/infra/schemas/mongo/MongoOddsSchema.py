

from main.domain.odds.Odds import Odds
from marshmallow import Schema, fields, post_load

from main.infra.schemas.field.CurrencyField import CurrencyField


class MongoOddsSchema(Schema):
    home_odds = fields.Float(required=True)
    away_odds = fields.Float(required=True)
    payout = CurrencyField(required=True)
    home_missing_amount = CurrencyField(required=True)
    away_missing_amount = CurrencyField(required=True)

    @post_load()
    def create_odds(self, data, **kwargs):
        return Odds(data["home_odds"], data["away_odds"], data["payout"], data["home_missing_amount"], data["away_missing_amount"])