from main.domain.purchase.Purchase import Purchase
from main.infra.schemas.field.MongoDomainIdField import MongoDomainIdField
from main.infra.schemas.field.CurrencyField import CurrencyField
from marshmallow import Schema, fields, post_load

class MongoPurchaseSchema(Schema):
    royale_coin_gain = CurrencyField(required=True)
    price = CurrencyField(required=True)
    id = MongoDomainIdField(data_key="_id", required=True)
    create_time = fields.DateTime(required=True)
    status = fields.String(required=True)
    customer_email = fields.String(required=True)
    payer_id = fields.String(required=True)
    name = fields.String(required=True)
    country_code = fields.String(required=True)
    order_id = fields.String(required=True)
    user_id = MongoDomainIdField(required=True)
        

    @post_load
    def create_purchase(self, data, **kwargs):
        return Purchase(**data)
