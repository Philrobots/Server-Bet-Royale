
from flask import request
from flask_restful import Resource
from main.api.schemas.response.BetResponseSchema import BetResponseSchema
from main.domain.identifiers.DomainId import DomainId

from main.infra.authentication.TokenDecoder import TokenDecoder
from main.service.BetService import BetService
from main.api.schemas.request.AcceptBetRequestSchema import AcceptBetRequestSchema


class AcceptBetResource(Resource):

    def __init__(self, token_decoder:TokenDecoder, bet_service:BetService, bet_response_schema: BetResponseSchema, accept_bet_request_schema: AcceptBetRequestSchema):
        self.token_decoder = token_decoder
        self.bet_service = bet_service
        self.bet_response_schema = bet_response_schema
        self.accept_bet_request_schema = accept_bet_request_schema

    def get(self):
        auth_token = request.headers.get("Authorization", "")
        user_id = DomainId(self.token_decoder.decode_auth_token(auth_token))
        bets = self.bet_service.get_accepted_bet(user_id)
        return self.bet_response_schema.dump(bets, many=True)
    
    def post(self):
        auth_token = request.headers.get("Authorization", "")
        user_id = self.token_decoder.decode_auth_token(auth_token)
        
        accept_bet_request_dict = request.json
        accept_bet_request_dict["user_id"] = user_id
        accept_bet_info = self.accept_bet_request_schema.load(accept_bet_request_dict)
        
        bet = self.bet_service.accept_bet(accept_bet_info)
        
        return self.bet_response_schema.dump(bet)