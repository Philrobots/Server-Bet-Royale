import datetime

import pytz
from main.domain.identifiers.DomainId import DomainId


class Gift:

    def __init__(self, id: DomainId, user_id: DomainId, price: float, can_receive: bool, time_last_gift: datetime, total_price_gift_receive: float, number_of_gift_receive: float) -> None:
        self.id = id
        self.user_id = user_id
        self.price = price
        self.can_receive = can_receive
        self.time_last_gift = time_last_gift
        self.total_price_gift_receive = total_price_gift_receive
        self.number_of_gift_receive = number_of_gift_receive
        
    def can_receive_gift(self):
        return self.can_receive
    
    def receive_gift(self) -> bool:
        if self.can_receive is False:
            return False
        self.can_receive = False
        self.time_last_gift = datetime.datetime.now(pytz.timezone('US/Eastern'))
        self.total_price_gift_receive += self.price
        self.number_of_gift_receive += 1
        return True