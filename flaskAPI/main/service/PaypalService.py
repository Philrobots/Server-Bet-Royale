import requests


class PaypalService:

    def __init__(self, paypal_api_url: str, paypal_api_token: str):
        self.paypal_api_url = paypal_api_url
        self.paypal_api_token = paypal_api_token

    def verify_if_order_id_exist(self, order_id: str):
        url = '{}/v2/checkout/orders/{}'.format(self.paypal_api_url, order_id)

        payload = {}
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer {}'.format(self.paypal_api_token)
        }

        try:
            response = requests.request("GET", url, headers=headers, data= payload)
            response_body = response.json()
            
            if response.status_code != 200 and response_body.name == "RESOURCE_NOT_FOUND":
                raise Exception("Error on paypal request. Order Id does not exist")
        except:
            raise Exception("Error on paypal request. Order Id does not exist")
