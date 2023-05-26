from main.domain.transaction.Transaction import Transaction
from main.domain.transaction.TransactionType import TransactionType
from main.infra.schemas.field.MongoDomainIdField import MongoDomainIdField
from main.infra.schemas.field.NullableCurrencyField import NullableCurrencyField
from main.infra.schemas.field.NullableMongoDomainIdField import NullableMongoDomainIdField
from main.infra.schemas.field.CurrencyField import CurrencyField
from marshmallow import Schema, fields, post_load

class MongoTransactionSchema(Schema):
    transaction_id = MongoDomainIdField(data_key="_id", required=True)
    user_id = MongoDomainIdField(required=True)
    amount = NullableCurrencyField(required=True, allow_none=True)
    transaction_type = fields.Enum(TransactionType, required=True)
    bet_id = NullableMongoDomainIdField(required=True, allow_none=True)
    date_created = fields.DateTime(required=True)
    current_balance = CurrencyField(required=True)

    @post_load
    def make_transaction(self, data, **kwargs):
        return Transaction(**data)
