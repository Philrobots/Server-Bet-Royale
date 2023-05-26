from main.domain.sports_game.bookmakers.OddsTeam import OddsTeam
from marshmallow import Schema, post_load, fields

class MongoOddsTeamSchema(Schema):
    odds = fields.Float(required=True)
    team = fields.String(required=True)
    is_home_team = fields.Bool(required=True)

    @post_load()
    def create_odds_team(self, data, **kwargs):
        return OddsTeam(**data)