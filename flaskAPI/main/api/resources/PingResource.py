from flask import jsonify
from flask_restful import Resource


class PingResource(Resource):

    def get(self):
        response = jsonify()
        response.status_code = 200
        return response
