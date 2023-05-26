
from flask import request, jsonify
from flask_restful import Resource
from main.api.schemas.response.BetResponseSchema import BetResponseSchema
from main.domain.identifiers.DomainId import DomainId

from main.infra.authentication.TokenDecoder import TokenDecoder
from main.service.BetService import BetService


class UserBetResource(Resource):

    def __init__(self, token_decoder: TokenDecoder, bet_service: BetService, bet_response_schema: BetResponseSchema):
        self.token_decoder = token_decoder
        self.bet_service = bet_service
        self.bet_response_schema = bet_response_schema

    def get(self):
        auth_token = request.headers.get("Authorization", "")
        user_id = DomainId(self.token_decoder.decode_auth_token(auth_token))
        user_open_bets = self.bet_service.get_user_open_bets(user_id)
        user_activte_bets = self.bet_service.get_user_active_bet(user_id=user_id)
        open_bets = self.bet_response_schema.dump(user_open_bets, many=True)
        activite_bets = self.bet_response_schema.dump(user_activte_bets, many=True)
        
        for active_bet in activite_bets:
            active_bet["is_owner"] = user_id.to_string() == active_bet["owner_id"]
        
        return jsonify({ "open_bets": open_bets, "active_bets": activite_bets})
