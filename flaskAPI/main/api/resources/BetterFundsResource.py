from flask import request, jsonify
from flask_restful import Resource
from main.api.schemas.request.AddBetterFundsRequestSchema import AddBetterFundsRequestSchema
from main.domain.identifiers.DomainId import DomainId

from main.infra.authentication.TokenDecoder import TokenDecoder
from main.service.BetterFundsService import BetterFundsService


class BetterFundsResource(Resource):

    def __init__(self, token_decoder:TokenDecoder, better_funds_service:BetterFundsService, add_better_funds_request_schema:AddBetterFundsRequestSchema):
        self.token_decoder = token_decoder
        self.better_funds_service = better_funds_service
        self.add_better_funds_request_schema = add_better_funds_request_schema

    def get(self):
        try:
            auth_token = request.headers.get("Authorization", "")
            user_id = DomainId(self.token_decoder.decode_auth_token(auth_token))

            response = jsonify(balance=float(self.better_funds_service.get_balance(user_id)))
            return response
        except:
            return jsonify(balance=0)