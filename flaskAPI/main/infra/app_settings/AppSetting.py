from main.domain.identifiers.DomainId import DomainId
from main.infra.app_settings.AppSettingType import AppSettingType


class AppSetting:
    def __init__(self, id:DomainId, enabled:bool, app_setting_type:AppSettingType, value:str, kwargs:dict):
        self.id = id
        self.enabled = enabled
        self.app_setting_type = app_setting_type
        self.value = value
        self.kwargs = kwargs
