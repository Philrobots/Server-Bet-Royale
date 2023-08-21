from main.domain.currency.Currency import Currency
from main.domain.gift.Gift import Gift
from main.domain.gift.GiftFactory import GiftFactory
from main.domain.identifiers.DomainId import DomainId
from main.infra.db.repository.GiftRepository import GiftRepository
from main.infra.exception.NonExistingGiftException import NonExistingGiftException
from main.service.BetterFundsService import BetterFundsService


class GiftService:
    
    def __init__(self, gift_repository: GiftRepository, gift_factory: GiftFactory, better_service: BetterFundsService) -> None:
        self.gift_repository = gift_repository
        self.gift_factory = gift_factory
        self.better_service = better_service
    
    def receive_gift(self, user_id: DomainId):
        gift = self.get_gift(user_id)
        received = gift.receive_gift()
        if received:
            self.better_service.add_funds(user_id, Currency(gift.price))
            self.gift_repository.update_gift(gift)
        return received
    
    def create_gift(self, user_id: DomainId) -> Gift:
        gift = self.gift_factory.create(user_id)
        self.gift_repository.add_gift(gift)
        return gift
        
    def get_gift(self, user_id: DomainId) -> Gift:
        try:
            return self.gift_repository.find_by_user_id(user_id)
        except NonExistingGiftException:
            return self.create_gift(user_id)
        
    def reset_all_gifts(self) -> None:
        self.gift_repository.reset_gift()