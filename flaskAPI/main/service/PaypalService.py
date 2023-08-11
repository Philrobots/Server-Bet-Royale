import logging
import requests
import base64

class PaypalService:

    def __init__(self, paypal_api_url: str, paypal_client_id: str, paypal_secret: str):
        self.paypal_api_url = paypal_api_url
        self.paypal_client_id = paypal_client_id
        self.paypal_secret = paypal_secret
        
    def verify_if_order_id_exist(self, order_id: str):
        
        credentials = '{}:{}'.format(self.paypal_client_id, self.paypal_secret)
        encode_credential = base64.b64encode(credentials.encode('utf-8')).decode('utf-8').replace("\n", "")
        
        headers = {
            "Authorization": "Basic {}".format(encode_credential),
            'Accept': 'application/json',
            'Accept-Language': 'en_US',
        }

        param = {
            'grant_type': 'client_credentials',
        }

        url = '{}/v2/checkout/orders/{}'.format(self.paypal_api_url, order_id)
        try:
            response = requests.request("GET", url, headers=headers, data=param)
            response_body = response.json()
            logging.info(response_body)
            
            if response.status_code != 200 and response_body.name == "RESOURCE_NOT_FOUND":
                raise Exception("Error on paypal request. Order Id does not exist")
        except:
            raise Exception("Error on paypal request. Order Id does not exist")
