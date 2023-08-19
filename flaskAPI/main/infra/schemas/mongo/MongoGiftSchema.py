from main.domain.gift.Gift import Gift
from marshmallow import Schema, fields,post_load
from main.infra.schemas.field.MongoDomainIdField import MongoDomainIdField


class MongoGiftSchema(Schema):
    id = MongoDomainIdField(data_key="_id", required=True)
    user_id = MongoDomainIdField(required=True)
    price = fields.Float(required=True)
    can_receive = fields.Bool(required=True)
    time_last_gift = fields.DateTime(required=False)
    total_price_gift_receive = fields.Float(required=True)
    number_of_gift_receive = fields.Float(required=True)
    
    @post_load
    def create_gift(self, data, **kwargs) -> Gift:
        return Gift(**data)