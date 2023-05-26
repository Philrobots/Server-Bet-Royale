


from flask_restful import Resource
from flask import request
from main.api.schemas.response.BetterStatsResponseSchema import BetterStatsResponseSchema

from main.domain.identifiers.DomainId import DomainId
from main.infra.authentication.TokenDecoder import TokenDecoder
from main.service.BetterStatsService import BetterStatsService


class TransactionResource(Resource):
    def __init__(self, token_decoder:TokenDecoder, better_stats_service: BetterStatsService, better_stats_response_schema:BetterStatsResponseSchema):
        self.token_decoder = token_decoder
        self.better_stats_service = better_stats_service
        self.better_stats_response_schema = better_stats_response_schema

    def get(self):
        auth_token = request.headers.get("Authorization", "")
        user_id = DomainId(self.token_decoder.decode_auth_token(auth_token))
        better_stats = self.better_stats_service.calculate_better_stats(user_id)
        return self.better_stats_response_schema.dump(better_stats)
