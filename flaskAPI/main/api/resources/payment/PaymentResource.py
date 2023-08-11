from flask import request
from flask_restful import Resource
from flask import request, jsonify
from main.api.resources.payment.CreatePurchaseRequestSchema import CreatePurchaseRequestSchema
from main.api.resources.payment.PurchaseResponseSchema import PurchaseResponseSchema
from main.domain.identifiers.DomainId import DomainId
from main.domain.purchase.CreatePurchaseInfo import CreatePurchaseInfo
from main.infra.authentication.TokenDecoder import TokenDecoder

from main.service.PaymentService import PaymentService

class PaymentResource(Resource):

    def __init__(self, payment_service: PaymentService, token_decoder: TokenDecoder, create_purchase_request_schema: CreatePurchaseRequestSchema, purchase_response_schema: PurchaseResponseSchema):
        self.payment_service = payment_service
        self.token_decoder = token_decoder
        self.create_purchase_request_schema = create_purchase_request_schema
        self.purchase_response_schema = purchase_response_schema

    def get(self):
        purchases = self.payment_service.findAll()
        
        return [self.purchase_response_schema.dump(purchase) for purchase in purchases]
    
    def post(self):
        auth_token = request.headers.get("Authorization", "")
        user_id = DomainId(self.token_decoder.decode_auth_token(auth_token))
        
        create_payment_dict = request.json
        create_payment_info: CreatePurchaseInfo = self.create_purchase_request_schema.load(create_payment_dict)
        create_payment_info.set_user_id(user_id)
        
        try:
            purchase = self.payment_service.create_payment(user_id, create_payment_info)
            return self.purchase_response_schema.dump(purchase)
        except Exception as e:
            return str(e), 400