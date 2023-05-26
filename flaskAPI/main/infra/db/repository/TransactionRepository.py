from typing import List

import pymongo
from main.domain.identifiers import DomainId
from main.infra.db.connector.MongoConnector import MongoConnector
from main.infra.schemas.mongo.MongoTransactionSchema import MongoTransactionSchema
from main.domain.transaction.Transaction import Transaction

class TransactionRepository:
    
    def __init__(self, transaction_schema: MongoTransactionSchema, connector: MongoConnector):
        self.transaction_schema = transaction_schema
        self.connector = connector
        self.db = self.connector.main.transactions
    
    
    def add_transaction(self, transaction: Transaction):
        transaction_dict = self.transaction_schema.dump(transaction)
        self.db.insert_one(transaction_dict)
    
    def get_transactions(self, user_id: DomainId) -> List[Transaction]:
        return [self.transaction_schema.load(transaction) for transaction in self.db.find({'user_id': user_id.to_object_id()}).sort('_id', pymongo.DESCENDING)]