from main.domain.identifiers.DomainId import DomainId
from main.infra.authentication.UserAuth import UserAuth


class UserAuthBuilder:

    def __init__(self):
        self.__username = "a_valid_username"
        # hash for password -> BijouPapoumonami1234
        self.__password_hash = "$2b$12$lJNdxsJgPGZKmzmQ3ecrxeZPmvHBYkwFYA4lZPBJ4SRzGjFzxtq4."
        self.__email = "email@email.com"
        self.__secret_key = "secretkey"
        self.__id = DomainId()

    def with_username(self, username):
        self.__username = username
        return self

    def with_password_hash(self, password_hash):
        self.__password_hash = password_hash
        return self

    def with_id(self, id):
        self.__id = id
        return self

    def with_secret_key(self, secret_key):
        self.__secret_key = secret_key
        return self

    def with_email(self, email):
        self.__email = email
        return self

    def build(self):
        return UserAuth(self.__username, self.__password_hash, self.__email, self.__id, self.__secret_key)
