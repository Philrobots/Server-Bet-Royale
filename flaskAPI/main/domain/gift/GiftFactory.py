from main.domain.gift.Gift import Gift
from main.domain.identifiers.DomainId import DomainId


class GiftFactory:
    
    def create(self, user_id: DomainId) -> Gift:
        return Gift(
            id=DomainId(),
            user_id=user_id,
            price=50,
            can_receive=True,
            time_last_gift=None,
            total_price_gift_receive=0,
            number_of_gift_receive=0
        )