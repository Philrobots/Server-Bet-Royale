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