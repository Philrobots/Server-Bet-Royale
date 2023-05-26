from main.domain.identifiers.DomainId import DomainId
from main.infra.authentication.UserAuth import UserAuth
from main.infra.db.connector.MongoConnector import MongoConnector
from main.infra.exception.NonExistingUserException import NonExistingUserException
from main.infra.schemas.mongo.MongoUserAuthSchema import MongoUserAuthSchema
from main.infra.exception.NonExistingEmailException import NonExistingEmailException


class UserAuthRepository:

    def __init__(self, user_auth_schema: MongoUserAuthSchema, connector: MongoConnector):
        self.connector = connector
        self.user_auth_schema = user_auth_schema
        self.db = self.connector.main.users

    def add_user(self, user_auth: UserAuth):
        user_auth_dict = self.user_auth_schema.dump(user_auth)
        self.db.insert_one(user_auth_dict)

    def get_by_id(self, user_id: DomainId) -> UserAuth:
        try:
            result = self.db.find_one({'_id': user_id.to_object_id()})
            if result is None:
                raise NonExistingUserException
            return self.user_auth_schema.load(result)
        except ValueError:
            raise NonExistingUserException

    def get_by_username(self, username) -> UserAuth:
        try:
            result = self.db.find_one({'username': username})
            if result is None:
                raise NonExistingUserException
            return self.user_auth_schema.load(result)
        except ValueError:
            raise NonExistingUserException

    def get_by_email(self, email) -> UserAuth:
        try:
            result = self.db.find_one({'email': email})
            if result is None:
                raise NonExistingEmailException
            return self.user_auth_schema.load(result)
        except ValueError:
            raise NonExistingEmailException
