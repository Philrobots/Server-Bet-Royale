from datetime import datetime
from main.domain.currency.Currency import Currency

from main.domain.identifiers.DomainId import DomainId


class CreatePurchaseInfo:
    
    def __init__(self, 
                 royale_coin_gain: float, create_time: datetime, status: str, 
                 customer_email: str, payer_id: str, name: str, country_code: str, 
                 price: float, order_id: str) -> None:
        self.royale_coin_gain = royale_coin_gain
        self.create_time = create_time
        self.status = status
        self.customer_email = customer_email
        self.payer_id = payer_id
        self.name = name
        self.country_code = country_code
        self.price = price
        self.order_id = order_id
        self.user_id = None
        
    def set_user_id(self, user_id: DomainId):
        self.user_id = user_id