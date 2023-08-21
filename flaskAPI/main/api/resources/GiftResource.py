import logging
from main.api.schemas.response.GiftResponseSchema import GiftResponseSchema
from main.domain.identifiers.DomainId import DomainId
from main.infra.authentication.TokenDecoder import TokenDecoder
from main.service.GiftService import GiftService
from flask import Response, request, jsonify
from flask_restful import Resource



class GiftResource(Resource):
    
    def __init__(self, gift_service: GiftService, gift_response_schema: GiftResponseSchema, token_decoder: TokenDecoder) -> None:
        self.gift_service = gift_service
        self.gift_response_schema = gift_response_schema
        self.token_decoder = token_decoder
        
    def get(self):
        auth_token = request.headers.get("Authorization", "")
        logging.info(auth_token)
        user_id = DomainId(self.token_decoder.decode_auth_token(auth_token))
        gift = self.gift_service.get_gift(user_id)
        return self.gift_response_schema.dump(gift), 200
    
    def post(self):
        auth_token = request.headers.get("Authorization", "")
        user_id = DomainId(self.token_decoder.decode_auth_token(auth_token))
        return self.gift_service.receive_gift(user_id)
        