
from flask import request, jsonify
from flask_restful import Resource
from main.api.schemas.request.CreateBetRequestSchema import CreateBetRequestSchema
from main.api.schemas.response.BetResponseSchema import BetResponseSchema
from main.domain.identifiers.DomainId import DomainId

from main.infra.authentication.TokenDecoder import TokenDecoder
from main.service.BetService import BetService


class BetWithIdResource(Resource):

    def __init__(self, token_decoder: TokenDecoder, bet_service: BetService):
        self.token_decoder = token_decoder
        self.bet_service = bet_service

    def delete(self, id:str):
        bet_id = DomainId(id)
        auth_token = request.headers.get("Authorization", "")
        user_id = DomainId(self.token_decoder.decode_auth_token(auth_token))
        self.bet_service.delete_bet(bet_id, user_id)
        response = jsonify()
        response.status_code = 200
        return response
