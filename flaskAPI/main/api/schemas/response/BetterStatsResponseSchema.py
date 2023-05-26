from marshmallow import Schema, fields

from main.api.schemas.response.TransactionInfoResponseSchema import TransactionInfoResponseSchema
class BetterStatsResponseSchema(Schema):
    wins = fields.Int(required=True)
    losses = fields.Int(required=True)
    win_rate = fields.Float(required=True)
    transaction_infos = fields.List(fields.Nested(TransactionInfoResponseSchema), data_key='transactions', required=True)
