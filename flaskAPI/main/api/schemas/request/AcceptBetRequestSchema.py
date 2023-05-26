
from main.domain.bet.AcceptBetInfo import AcceptBetInfo
from marshmallow import Schema, post_load

from main.api.schemas.field.IdField import IdField


class AcceptBetRequestSchema(Schema):
    bet_id = IdField(required=True)
    user_id = IdField(required=True)

    @post_load()
    def create_sports_game(self, data, **kwargs):
        return AcceptBetInfo(**data)

