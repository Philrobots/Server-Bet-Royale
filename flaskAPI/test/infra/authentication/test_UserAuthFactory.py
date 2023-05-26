import unittest

from mockito import when, mock
from main.infra.db.repository.UserAuthRepository import UserAuthRepository
from main.infra.authentication.UserAuthFactory import UserAuthFactory
from test.infra.builder.UserAuthBuilder import UserAuthBuilder
from main.infra.exception.UsernameAlreadyTakenException import UsernameAlreadyTakenException
from main.infra.exception.NonExistingUserException import NonExistingUserException
from main.infra.exception.InvalidPasswordFormatException import InvalidPasswordFormatException
from main.infra.exception.InvalidUsernameFormatException import InvalidUsernameFormatException

from main.infra.exception.EmailAlreadyTakenException import EmailAlreadyTakenException

from main.infra.exception.NonExistingEmailException import NonExistingEmailException

from main.infra.exception.InvalidEmailFormatException import InvalidEmailFormatException


class UserAuthFactoryTest(unittest.TestCase):

    def setUp(self):
        self.EXISTING_USERNAME = "existing"
        self.NON_EXISTING_USERNAME = "non_existing"
        self.VALID_EMAIL = "email@email.com"
        self.TAKEN_EMAIL = "taken@email.com"
        self.INVALID_EMAIL = "email@.com"
        self.A_PASSWORD = "AValidPassword1234"
        self.A_SECRET_KEY = "secret"
        self.A_USER = UserAuthBuilder().build()
        self.user_repo = mock(UserAuthRepository)
        self.user_factory = UserAuthFactory(self.user_repo, self.A_SECRET_KEY)

    def test_givenExistingUsername_whenCreate_thenRaisesUsernameAlreadyTakenException(self):
        when(self.user_repo).get_by_username(self.EXISTING_USERNAME).thenReturn(self.A_USER)

        with self.assertRaises(UsernameAlreadyTakenException):
            self.user_factory.create(self.EXISTING_USERNAME, self.A_PASSWORD, self.VALID_EMAIL)

    def test_givenExistingEmail_whenCreate_thenRaisesEmailAlreadyTakenException(self):
        when(self.user_repo).get_by_username(self.NON_EXISTING_USERNAME).thenRaise(NonExistingUserException)
        when(self.user_repo).get_by_email(self.TAKEN_EMAIL).thenReturn(self.A_USER)

        with self.assertRaises(EmailAlreadyTakenException):
            self.user_factory.create(self.NON_EXISTING_USERNAME, self.A_PASSWORD, self.TAKEN_EMAIL)

    def test_whenCreate_thenCreatesUserObjectWithSameUsernameAndEmail(self):
        when(self.user_repo).get_by_username(self.NON_EXISTING_USERNAME).thenRaise(NonExistingUserException)
        when(self.user_repo).get_by_email(self.VALID_EMAIL).thenRaise(NonExistingEmailException)

        actual_user = self.user_factory.create(self.NON_EXISTING_USERNAME, self.A_PASSWORD, self.VALID_EMAIL)

        self.assertEqual(self.NON_EXISTING_USERNAME, actual_user.username)
        self.assertEqual(self.VALID_EMAIL, actual_user.email)

    def test_whenCreate_thenCreatesUserObjectWithValidHashPassword(self):
        when(self.user_repo).get_by_username(self.NON_EXISTING_USERNAME).thenRaise(NonExistingUserException)
        when(self.user_repo).get_by_email(self.VALID_EMAIL).thenRaise(NonExistingEmailException)

        actual_user = self.user_factory.create(self.NON_EXISTING_USERNAME, self.A_PASSWORD, self.VALID_EMAIL)
        invalid_password = "invalid"

        self.assertTrue(actual_user.authenticate(self.A_PASSWORD))
        self.assertFalse(actual_user.authenticate(invalid_password))

    def test_givenInvalidPasswordWithNoCapitals_whenCreateObject_thenRaisesInvalidPasswordFormatException(self):
        when(self.user_repo).get_by_username(self.NON_EXISTING_USERNAME).thenRaise(NonExistingUserException)
        when(self.user_repo).get_by_email(self.VALID_EMAIL).thenRaise(NonExistingEmailException)

        invalid_password = "pasdemajusculesdanscemdp"
        with self.assertRaises(InvalidPasswordFormatException):
            self.user_factory.create(self.NON_EXISTING_USERNAME, invalid_password, self.VALID_EMAIL)

    def test_givenInvalidUsernameWithInvalidCharacter_whenCreateObject_thenRaisesInvalidUsernameFormatException(self):
        invalid_username = "Caractèresinvalides$$%"
        when(self.user_repo).get_by_username(invalid_username).thenRaise(NonExistingUserException)
        when(self.user_repo).get_by_email(self.VALID_EMAIL).thenRaise(NonExistingEmailException)

        with self.assertRaises(InvalidUsernameFormatException):
            self.user_factory.create(invalid_username, self.A_PASSWORD, self.VALID_EMAIL)

    def test_givenInvalidEmailWithInvalidCharacter_whenCreateObject_thenRaisesInvalidUsernameFormatException(self):
        when(self.user_repo).get_by_username(self.NON_EXISTING_USERNAME).thenRaise(NonExistingUserException)
        when(self.user_repo).get_by_email(self.INVALID_EMAIL).thenRaise(NonExistingEmailException)

        with self.assertRaises(InvalidEmailFormatException):
            self.user_factory.create(self.NON_EXISTING_USERNAME, self.A_PASSWORD, self.INVALID_EMAIL)
