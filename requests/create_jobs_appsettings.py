import pymongo
from bson import ObjectId
mongo_client = pymongo.MongoClient("mongodb://root:golf123@localhost:27017/")
def main():
    mongo_client.main.app_settings.insert_one({
  "_id": ObjectId("63fe83fe00b4a69bbcfdd8cb"),
  "app_setting_type": "JOB",
  "enabled": True,
  "value": "SportsGameScheduler.get_new_live_games",
  "kwargs": {
    "trigger": "interval",
    "minutes": 9,
    "id": "get_new_live_games"
  }
})
    mongo_client.main.app_settings.insert_one({
  "_id": ObjectId("63fe83fe00b4a69bbcfdd8cc"),
  "app_setting_type": "JOB",
  "enabled": True,
  "value": "BetScheduler.complete_bets",
  "kwargs": {
    "trigger": "interval",
    "minutes": 10,
    "id": "complete_bets"
  }
})
    pass

if __name__ == "__main__":
    main()