from main.domain.identifiers.DomainId import DomainId
from main.domain.purchase.CreatePurchaseInfo import CreatePurchaseInfo
from main.domain.purchase.Purchase import Purchase
from main.domain.purchase.PurchaseFactory import PurchaseFactory
from main.infra.db.repository.BetterRepository import BetterRepository
from main.infra.db.repository.PurchaseRepository import PurchaseRepository


class PaymentService:
    
    def __init__(self, purchase_repository: PurchaseRepository, better_repository: BetterRepository, purchase_factory: PurchaseFactory):
        self.purchase_repository = purchase_repository
        self.purchase_factory = purchase_factory
        self.better_repository = better_repository
    
    def findAll(self) -> list[Purchase]:
        return self.purchase_repository.get_purchases()
    
    def create_payment(self, user_id: DomainId, create_purchase_info: CreatePurchaseInfo) -> Purchase:
        purchase = self.purchase_factory.create(create_purchase_info)
        self.purchase_repository.create_purchase(purchase)
        
        better = self.better_repository.get_by_id(user_id)
        better.add_funds(purchase.royale_coin_gain)
        self.better_repository.update_better(better)
        
        return purchase
        