from asyncio.log import logger
import logging
from main.domain.gift.Gift import Gift
from main.domain.identifiers.DomainId import DomainId
from main.infra.db.connector.MongoConnector import MongoConnector
from main.infra.exception.NonExistingGiftException import NonExistingGiftException
from main.infra.schemas.mongo.MongoGiftSchema import MongoGiftSchema


class GiftRepository:
    
    def __init__(self, mongo_gift_schema: MongoGiftSchema, connector: MongoConnector):
        self.connector = connector
        self.mongo_gift_schema = mongo_gift_schema
        self.db = self.connector.main.gifts
        
    def add_gift(self, gift: Gift) -> None:
        gift_dict = self.mongo_gift_schema.dump(gift)
        self.db.insert_one(gift_dict)
        
    def find_by_user_id(self, user_id: DomainId) -> Gift:
        try:
            result = self.db.find_one({'user_id': user_id.to_object_id()})
            if result is None:
                raise NonExistingGiftException
            return self.mongo_gift_schema.load(result)        
        except ValueError:
            raise NonExistingGiftException
        
    def update_gift(self, gift: Gift) -> None:
        gift_dict = self.mongo_gift_schema.dump(gift)
        self.db.replace_one({'_id': gift.id.to_object_id()}, gift_dict)
        
    def reset_gift(self) -> None:
        result = self.db.update_many({}, {'$set': {'can_receive': True}})
        logging.info("All gifts have been reset : {}".format(result.modified_count))
        
