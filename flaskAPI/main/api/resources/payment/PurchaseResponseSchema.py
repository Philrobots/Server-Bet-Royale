from main.infra.schemas.mongo.MongoBookMakerSchema import MongoBookMakerSchema
from marshmallow import Schema, fields
from main.api.schemas.field.IdField import IdField


class PurchaseResponseSchema(Schema):
    id = IdField(required=True)
    status = fields.String(required=True)
    customer_email = fields.String(required=True)
    create_time = fields.AwareDateTime(required=True, allow_none=True)
    name = fields.String(required=True)
    royale_coin_gain = fields.Float(required=True)
    payer_id = fields.String(required=True)
    price = fields.Float(required=True)
    
    