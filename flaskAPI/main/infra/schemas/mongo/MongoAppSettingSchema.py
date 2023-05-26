from marshmallow import Schema, fields, post_load
from main.infra.app_settings.AppSetting import AppSetting
from main.infra.schemas.field.MongoDomainIdField import MongoDomainIdField
from main.infra.app_settings.AppSettingType import AppSettingType


class MongoAppSettingSchema(Schema):
    id = MongoDomainIdField(data_key="_id", required=True)
    enabled = fields.Bool(required=True)
    app_setting_type = fields.Enum(AppSettingType, required=True)
    value = fields.Str(required=True)
    kwargs = fields.Dict()

    @post_load
    def make_app_setting(self, data, **kwargs):
        return AppSetting(**data)