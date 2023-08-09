from datetime import datetime
from main.domain.identifiers.DomainId import DomainId
from main.domain.currency.Currency import Currency

class Purchase:
    
    def __init__(self,  id: DomainId, royale_coin_gain: Currency, create_time: datetime, status: str, 
                 customer_email: str, payer_id: str, name: str, country_code: str, price: Currency, order_id: str, 
                 user_id: DomainId) -> None:
        self.user_id = user_id
        self.royale_coin_gain = royale_coin_gain
        self.id = id
        self.create_time = create_time
        self.status = status
        self.customer_email = customer_email
        self.payer_id = payer_id
        self.name = name
        self.country_code = country_code
        self.price = price
        self.order_id = order_id
        
        