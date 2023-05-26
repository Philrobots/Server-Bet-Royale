import re

import bcrypt
from main.domain.identifiers.DomainId import DomainId
from main.infra.authentication.UserAuth import UserAuth
from main.infra.exception.EmailAlreadyTakenException import EmailAlreadyTakenException
from main.infra.exception.InvalidEmailFormatException import InvalidEmailFormatException
from main.infra.exception.InvalidPasswordFormatException import InvalidPasswordFormatException
from main.infra.exception.InvalidUsernameFormatException import InvalidUsernameFormatException
from main.infra.exception.NonExistingEmailException import NonExistingEmailException
from main.infra.exception.NonExistingUserException import NonExistingUserException
from main.infra.exception.UsernameAlreadyTakenException import UsernameAlreadyTakenException


class UserAuthFactory:

    def __init__(self, user_repository, secret_key):
        # Password Minimum eight characters, at least one letter and one number:
        self._PASSWORD_REGEX = r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d@$!%*#?&]{8,}$"
                                
        # Username of length 6-16 with alphanumeric, underscore and hyphen
        self._USERNAME_REGEX = r"^[a-zA-Z0-9_-]{6,16}$"
        # Email with string@string.string
        self._EMAIL_REGEX = r"^\S+@\S+\.\S+$"
        self.user_repository = user_repository
        self.secret_key = secret_key

    def create(self, username, password, email) -> UserAuth:
        try:
            self.user_repository.get_by_username(username)
            raise UsernameAlreadyTakenException
        except NonExistingUserException:
            pass

        try:
            self.user_repository.get_by_email(email)
            raise EmailAlreadyTakenException
        except NonExistingEmailException:
            pass

        return UserAuth(self._validate_username(username), self._validate_and_hash_password(password), self._validate_email(email), DomainId(),
                        self.secret_key)

    def _validate_and_hash_password(self, password):
        if re.match(self._PASSWORD_REGEX, password):
            return bcrypt.hashpw(password.encode("UTF-8"), bcrypt.gensalt()).decode("UTF-8")
        raise InvalidPasswordFormatException

    def _validate_username(self, username):
        if re.match(self._USERNAME_REGEX, username):
            return username
        raise InvalidUsernameFormatException

    def _validate_email(self, email):
        if re.match(self._EMAIL_REGEX, email):
            return email
        raise InvalidEmailFormatException
