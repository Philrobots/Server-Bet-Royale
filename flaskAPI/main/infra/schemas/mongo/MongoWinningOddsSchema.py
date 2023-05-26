

from main.domain.odds.Odds import Odds
from main.domain.sports_game.bookmakers.OddsTeam import OddsTeam
from marshmallow import Schema, fields, post_load

from main.infra.schemas.field.CurrencyField import CurrencyField


class MongoWinningOddsSchema(Schema):
    odds = fields.Float(required=True)
    is_home_team = fields.Boolean(required=True)
    team = fields.String(required=True)

    @post_load()
    def create_odds(self, data, **kwargs):
        return OddsTeam(**data)