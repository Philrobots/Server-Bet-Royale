import unittest

from main.domain.identifiers.DomainId import DomainId
from main.infra.authentication.TokenDecoder import TokenDecoder
from main.infra.exception.InvalidTokenException import InvalidTokenException
from test.infra.builder.UserAuthBuilder import UserAuthBuilder


class TokenDecoderTest(unittest.TestCase):

    def setUp(self):
        self.A_SECRET_KEY = "secret"
        self.A_USER_ID = DomainId()
        self.A_USER_AUTH = UserAuthBuilder().with_secret_key(self.A_SECRET_KEY).with_id(self.A_USER_ID).build()
        self.token_decoder = TokenDecoder(self.A_SECRET_KEY)

    def test_whenDecodeAuthToken_thenShouldReturnUserId(self):
        token = self.A_USER_AUTH.create_auth_token()

        user_id_string = self.token_decoder.decode_auth_token(token.to_string())

        self.assertEqual(user_id_string, self.A_USER_ID.to_string())

    def test_givenInvalidToken_thenShouldRaiseExpiredTokenException(self):
        invalid_token = "invalid"
        with self.assertRaises(InvalidTokenException):
            self.token_decoder.decode_auth_token(invalid_token)
