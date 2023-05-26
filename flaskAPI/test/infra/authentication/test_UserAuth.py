import unittest
import datetime
from jwt import encode
from main.domain.identifiers.DomainId import DomainId
from test.infra.builder.UserAuthBuilder import UserAuthBuilder


class UserAuthTest(unittest.TestCase):

    def setUp(self):
        self.VALID_PASSWORD = "BijouPapoumonami1234"
        self.A_USER_ID = DomainId()
        self.A_SECRET_KEY = "secret"
        self.user = UserAuthBuilder().with_secret_key(self.A_SECRET_KEY).with_id(self.A_USER_ID).build()

    def test_whenAuthenticate_thenAuthenticatesSuccesfully(self):
        authenticated = self.user.authenticate(self.VALID_PASSWORD)

        self.assertTrue(authenticated)

    def test_givenIncorrectPassword_whenAuthenticate_thenDoesNotAuthenticate(self):
        incorrect_password = "salut234"

        authenticated = self.user.authenticate(incorrect_password)

        self.assertFalse(authenticated)

    def test_whenCreateAuthToken_thenHasReturnsValidAuthToken(self):
        payload = {'iat': datetime.datetime.utcnow(), 'sub': self.A_USER_ID.to_string()}
        expected_string_token = encode(payload, self.A_SECRET_KEY, algorithm='HS256')

        actual_token = self.user.create_auth_token()

        self.assertEqual(expected_string_token, actual_token.to_string())
