

from ctypes import Array
from main.domain.identifiers.DomainId import DomainId
from main.domain.sports_game.SportsGame import SportsGame
from main.infra.db.connector.MongoConnector import MongoConnector
from main.infra.exception.NonExistingSportsGameException import NonExistingSportsGameException
from main.infra.exception.SportsGameNotUpdatedException import SportsGameNotUpdatedException
from main.infra.schemas.mongo.MongoSportsGameSchema import MongoSportsGameSchema
from datetime import datetime, timedelta
import pytz
import logging


class SportsGameRepository:

    def __init__(self, sports_game_schema: MongoSportsGameSchema, connector: MongoConnector):
        self.connector = connector
        self.sports_game_schema = sports_game_schema
        self.db = self.connector.main.sports_game

    def add_sports_game(self, sports_game: SportsGame):
        sports_game_dict = self.sports_game_schema.dump(sports_game)
        self.db.insert_one(sports_game_dict)

    def get_by_id(self, sport_game_id: DomainId):
        try:
            result = self.db.find_one({'_id': sport_game_id.to_object_id()})
            if result is None:
                raise NonExistingSportsGameException
            return self.sports_game_schema.load(result)
        except ValueError:
            raise NonExistingSportsGameException
        
    def get_active_game(self) -> Array[SportsGame]:
        return [self.sports_game_schema.load(sports_game) for sports_game in self.db.find({"completed": False })]
        
    def get_nfl_games(self) -> Array[SportsGame]:
        return [self.sports_game_schema.load(sports_game) for sports_game in self.db.find({"completed": False, "sport": "americanfootball"})]

    def get_hockey_games(self) -> Array[SportsGame]:
        return [self.sports_game_schema.load(sports_game) for sports_game in self.db.find({"completed": False, "sport": "icehockey"})]

    def get_basketball_games(self) -> Array[SportsGame]:
        return [self.sports_game_schema.load(sports_game) for sports_game in self.db.find({"completed": False, "sport": "basketball"})]

    def get_mlb_games(self) -> Array[SportsGame]:
        return [self.sports_game_schema.load(sports_game) for sports_game in self.db.find({"completed": False, "sport": "baseball"})]

    def get_mma_games(self) -> Array[SportsGame]:
        return [self.sports_game_schema.load(sports_game) for sports_game in self.db.find({"completed": False, "sport": "mma"})]

    def get_mls_games(self) -> Array[SportsGame]:
        return [self.sports_game_schema.load(sports_game) for sports_game in self.db.find({"completed": False, "sport": "soccer"})]

    def get_by_external_id(self, external_id: str) -> SportsGame:
        try:
            result = self.db.find_one({'external_id': external_id})
            if result is None:
                raise NonExistingSportsGameException
            return self.sports_game_schema.load(result)
        except ValueError:
            raise NonExistingSportsGameException

    def delete_sports_game(self, sports_game: SportsGame) -> None:
        try:
            self.db.delete_one({'_id': sports_game.id.to_object_id()})
        except ValueError:
            raise NonExistingSportsGameException

    def update_sports_game(self, sports_game: SportsGame):
        sports_game_dict = self.sports_game_schema.dump(sports_game)
        sport_game_id = sports_game.id
        result = self.db.replace_one(
            {'_id': sport_game_id.to_object_id()}, sports_game_dict)

        if result.modified_count == 0:
            raise SportsGameNotUpdatedException

    def insert_or_update_sports_game(self, sports_game: SportsGame):
        sports_game_dict = self.sports_game_schema.dump(sports_game)
        sports_game_external_id = sports_game_dict["external_id"]

        result = self.db.find_one({"external_id": sports_game_external_id})
        if result is None:
            self.db.insert_one(sports_game_dict)
        else:
            del sports_game_dict["_id"]
            if sports_game_dict["book_makers"] is None:
                sports_game_dict["book_makers"] = result["book_makers"]

            self.db.replace_one(
                {"external_id": sports_game_external_id}, sports_game_dict)

    def remove_old_games(self) -> int:
        now = datetime.now()
        last_month = now - timedelta(days=30)
        string_date = last_month.strftime("%Y-%m-%d %H:%M:%S")

        filter = {
            'game_start': {
                '$lte': string_date
            }
        }
        
        results = self.db.delete_many(filter=filter)
        
        return results.deleted_count
       
