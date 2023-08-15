from main.api.schemas.field.IdField import IdField
from main.domain.purchase.CreatePurchaseInfo import CreatePurchaseInfo
from main.infra.schemas.field.CurrencyField import CurrencyField
from marshmallow import Schema, fields, post_load


class CreatePurchaseRequestSchema(Schema):
    order_id = fields.String(required=True)   
    royale_coin_gain = fields.Float(required=True)  
    create_time = fields.DateTime(required=True)
    status = fields.String(required=True)
    customer_email = fields.String(required=True)
    payer_id = fields.String(required=True)         
    name = fields.String(required=True)    
    country_code = fields.String(required=True)    
    price = fields.Float(required=True) 
    
    @post_load()
    def create_purchase_info(self, data, **kwargs):
        return CreatePurchaseInfo(**data)

