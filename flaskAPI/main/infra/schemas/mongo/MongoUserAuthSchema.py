from marshmallow import Schema, fields, post_load

from main.infra.authentication.UserAuth import UserAuth
from main.infra.schemas.field.MongoDomainIdField import MongoDomainIdField


class MongoUserAuthSchema(Schema):

    def __init__(self, secret_key):
        super().__init__()
        self.secret_key = secret_key

    user_id = MongoDomainIdField(data_key="_id", required=True)
    username = fields.String(required=True)
    password = fields.String(required=True)
    email = fields.String(required=True)
    confirmed = fields.Boolean(required=True)

    @post_load()
    def create_user(self, data, **kwargs):
        return UserAuth(**data, secret_key=self.secret_key)
