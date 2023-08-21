from main.service.GiftService import GiftService


class GiftScheduler:
    
    def __init__(self, gift_service: GiftService) -> None:
        self.gift_service = gift_service
        
    def reset_all_gifts(self):
        self.gift_service.reset_all_gifts()