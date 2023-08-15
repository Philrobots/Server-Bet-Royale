import bcrypt
from main.domain.identifiers.DomainId import DomainId
from main.infra.authentication.Token import Token
import math as m
import random as r

class UserAuth:

    def __init__(self, username, password, email, user_id: DomainId, secret_key, confirmed):
        self.username = username
        self.password = password
        self.email = email
        self.user_id = user_id
        self._secret_key = secret_key
        self.confirmed = confirmed

    def authenticate(self, non_hashed_password):
        return bcrypt.checkpw(non_hashed_password.encode("UTF-8"), self.password.encode("UTF-8"))

    def create_auth_token(self) -> Token:
        return Token(self.user_id.to_string(), self._secret_key)

    def get_user_id(self) -> DomainId:
        return self.user_id
    
    def confirm_user(self) -> None:
        self.confirmed = True
    
    def is_confirmed(self) -> bool:
        return self.confirmed
