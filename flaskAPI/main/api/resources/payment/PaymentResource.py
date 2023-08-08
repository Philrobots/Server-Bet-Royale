from flask import request
from flask_restful import Resource
from flask import request, jsonify
import stripe
import os

class PaymentResource(Resource):

    def __init__(self):
        stripe.api_key = os.environ.get('STRIPE_SK')
        self.domain = os.environ.get('CLIENT_DOMAIN')

    def post(self):
        try:
            product_price_id = request.json.get('product_id')
            return jsonify(stripe.checkout.Session.create(
                line_items=[
                    {
                        'price': product_price_id,
                        'quantity': 1,
                    },
                ],
                mode='payment',
                success_url=self.domain + '/success',
                cancel_url=self.domain + '/cancel',
            ))
        except Exception as e:
            return str(e)
