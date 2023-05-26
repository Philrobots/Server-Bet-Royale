
from flask import request, jsonify
from flask_restful import Resource
from main.api.schemas.request.CreateBetRequestSchema import CreateBetRequestSchema
from main.api.schemas.response.BetResponseSchema import BetResponseSchema
from main.domain.identifiers.DomainId import DomainId

from main.infra.authentication.TokenDecoder import TokenDecoder
from main.service.BetService import BetService


class BetResource(Resource):

    def __init__(self, token_decoder: TokenDecoder, bet_service: BetService, create_bet_request_schema: CreateBetRequestSchema, bet_response_schema: BetResponseSchema):
        self.token_decoder = token_decoder
        self.bet_service = bet_service
        self.create_bet_request_schema = create_bet_request_schema
        self.bet_response_schema = bet_response_schema

    def post(self):
        auth_token = request.headers.get("Authorization", "")
        user_id = DomainId(self.token_decoder.decode_auth_token(auth_token))
        bet_request_dict = request.json
        loaded_dict = self.create_bet_request_schema.load(bet_request_dict)

        self.bet_service.create_bet(loaded_dict["sports_game_id"], user_id, loaded_dict["bet_amount"],
                                    loaded_dict["odds"], loaded_dict["is_home_bet"])

        response = jsonify()
        response.status_code = 201
        return response

    def get(self):
        all_bets = self.bet_service.get_open_bets()
        return self.bet_response_schema.dump(all_bets, many=True)

    def delete(self, id):
        auth_token = request.headers.get("Authorization", "")
        user_id = DomainId(self.token_decoder.decode_auth_token(auth_token))
        self.bet_service.delete_bet(id, user_id)
        response = jsonify()
        response.status_code = 200
        return response
