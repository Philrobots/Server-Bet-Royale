import jwt
import datetime


class Token:

    def __init__(self, user_id, secret_key):
        payload = {'iat': datetime.datetime.utcnow(), 'sub': user_id}
        self.token = jwt.encode(payload, secret_key, algorithm='HS256')

    def to_string(self):
        return self.token
