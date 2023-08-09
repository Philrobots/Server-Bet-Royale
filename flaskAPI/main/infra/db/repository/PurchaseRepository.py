import logging
from main.domain.identifiers.DomainId import DomainId
from main.domain.purchase.Purchase import Purchase
from main.infra.schemas.mongo.MongoPurchaseSchema import MongoPurchaseSchema
from main.infra.db.connector.MongoConnector import MongoConnector


class PurchaseRepository:

    def __init__(self, purchase_schema: MongoPurchaseSchema, connector: MongoConnector):
        self.mongo_purchase_schema = purchase_schema
        self.connector = connector
        self.db = self.connector.main.purchases
        
    def create_purchase(self, purchase: Purchase):
        purchase_dict = self.mongo_purchase_schema.dump(purchase)
        self.db.insert_one(purchase_dict)
    
    def get_purchases(self) -> list[Purchase]:
        return [self.mongo_purchase_schema.load(purchase) for purchase in self.db.find()]

    def verify_order_id_is_unique(self, order_id: str):
        purchase = self.db.find({'paypal_id': order_id})
        logging.info(purchase)
        if (purchase is not None):
            raise Exception("Paypal order already exists")