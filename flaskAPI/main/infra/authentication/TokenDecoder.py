from jwt import InvalidTokenError, decode

from main.infra.exception.InvalidTokenException import InvalidTokenException


class TokenDecoder:

    def __init__(self, secret_key):
        self.secret_key = secret_key

    def decode_auth_token(self, auth_token: str) -> str:
        try:
            payload = decode(auth_token, self.secret_key, algorithms="HS256")
            return payload['sub']
        except InvalidTokenError:
            raise InvalidTokenException
