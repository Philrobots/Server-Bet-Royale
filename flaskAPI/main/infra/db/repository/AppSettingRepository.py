from typing import List
from main.infra.app_settings.AppSetting import AppSetting
from main.infra.db.connector.MongoConnector import MongoConnector
from main.infra.schemas.mongo.MongoAppSettingSchema import MongoAppSettingSchema


class AppSettingRepository:

    def __init__(self, app_setting_schema: MongoAppSettingSchema, connector: MongoConnector):
        self.connector = connector
        self.app_setting_schema = app_setting_schema
        self.db = self.connector.main.app_settings

    def get_jobs(self) -> List[AppSetting]:
        return [self.app_setting_schema.load(app_setting) for app_setting in self.db.find({'app_setting_type': 'JOB', "enabled": True})]