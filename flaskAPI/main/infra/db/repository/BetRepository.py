

from typing import List
from main.domain.bet.Bet import Bet
from main.domain.identifiers.DomainId import DomainId
from main.infra.db.connector.MongoConnector import MongoConnector
from main.infra.exception.BetNotUpdatedException import BetNotUpdatedException
from main.infra.exception.NonExistingBetException import NonExistingBetException
from main.infra.schemas.mongo.MongoBetSchema import MongoBetSchema


class BetRepository:
    def __init__(self, bet_schema: MongoBetSchema, connector: MongoConnector):
        self.connector = connector
        self.bet_schema = bet_schema
        self.db = self.connector.main.bets

    def add_bet(self, bet: Bet):
        bet_dict = self.bet_schema.dump(bet)
        self.db.insert_one(bet_dict)

    def get_by_user_id(self, user_id: DomainId) -> Bet:
        try:
            result = self.db.find_one({'user_id': user_id.to_object_id()})
            if result is None:
                raise NonExistingBetException
            return self.better_schema.load(result)
        except ValueError:
            raise NonExistingBetException
        

    def get_all(self) -> List[Bet]:
        return [self.bet_schema.load(bet) for bet in self.db.find({})]
    
    def get_open_bet(self) -> List[Bet]:
        return [self.bet_schema.load(bet) for bet in self.db.find({ "is_accepted": False , "is_completed": False})]

    def get_completable_bets(self) -> List[Bet]:
        return [self.bet_schema.load(bet) for bet in self.db.find({ "is_completed": False})]
    
    def get_user_open_bet(self, user_id: DomainId) -> List[Bet]:
        return [self.bet_schema.load(bet) for bet in self.db.find({ "is_accepted": False, "owner_id": user_id.to_object_id(), "is_completed": False })]
    
    def get_user_active_bet(self, user_id: DomainId) -> List[Bet]:
        return [self.bet_schema.load(bet) for bet in self.db.find({ "is_accepted": True, "owner_id": user_id.to_object_id(), "is_completed": False })]
    
    def get_by_sports_game_id(self, sport_game_id: DomainId) -> list[Bet]:
        return [self.bet_schema.load(bet) for bet in self.db.find({ "sports_game_id": sport_game_id.to_object_id() })]
        
    
    def get_by_id(self, bet_id: DomainId) -> Bet:
        try:
            result = self.db.find_one({'_id': bet_id.to_object_id()})
            if result is None:
                raise NonExistingBetException
            return self.bet_schema.load(result)
        except ValueError:
            raise NonExistingBetException

    def update_bet(self, bet: Bet):
        bet_dict = self.bet_schema.dump(bet)
        bet_id = bet.id
        result = self.db.replace_one({'_id': bet_id.to_object_id()}, bet_dict)
        if result.modified_count == 0:
            raise BetNotUpdatedException

    def delete_bet(self, bet_id:DomainId):
        try:
            self.db.delete_one({'_id': bet_id.to_object_id()})
        except ValueError:
            raise NonExistingBetException
