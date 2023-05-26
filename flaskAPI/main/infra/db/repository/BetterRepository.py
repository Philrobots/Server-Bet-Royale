from main.infra.schemas.mongo.MongoBetterSchema import MongoBetterSchema
from main.domain.bet.Better import Better
from main.domain.identifiers.DomainId import DomainId
from main.infra.db.connector.MongoConnector import MongoConnector
from main.infra.exception.NonExistingUserException import NonExistingUserException


class BetterRepository:

    def __init__(self, better_schema: MongoBetterSchema, connector: MongoConnector):
        self.connector = connector
        self.better_schema = better_schema
        self.db = self.connector.main.betters

    def add_better(self, better: Better):
        better_dict = self.better_schema.dump(better)
        self.db.insert_one(better_dict)
        
    def get_leaders(self) -> list[Better]:
        return [self.better_schema.load(better) for better in self.db.find().sort('bank_balance', -1).limit(10)]

    def get_by_id(self, user_id: DomainId) -> Better:
        try:
            result = self.db.find_one({'_id': user_id.to_object_id()})
            if result is None:
                raise NonExistingUserException
            return self.better_schema.load(result)
        except ValueError:
            raise NonExistingUserException


    def update_better(self, better:Better):
        better_dict = self.better_schema.dump(better)
        better_id = better.user_id
        self.db.replace_one({'_id': better_id.to_object_id()}, better_dict)
