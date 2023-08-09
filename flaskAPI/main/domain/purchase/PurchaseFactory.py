from datetime import datetime
from main.domain.currency.Currency import Currency
from main.domain.identifiers.DomainId import DomainId
from main.domain.purchase.CreatePurchaseInfo import CreatePurchaseInfo
from main.domain.purchase.Purchase import Purchase


class PurchaseFactory:

    def create(self, create_purchase_info: CreatePurchaseInfo) -> Purchase:
        return Purchase(
            id=DomainId(),
            royale_coin_gain=Currency(create_purchase_info.royale_coin_gain),
            create_time=create_purchase_info.create_time,
            status=create_purchase_info.status,
            customer_email=create_purchase_info.customer_email,
            payer_id=create_purchase_info.payer_id,
            name=create_purchase_info.name,
            country_code=create_purchase_info.country_code,
            price=Currency(create_purchase_info.price, "USD"),
            order_id=create_purchase_info.order_id,
            user_id=create_purchase_info.user_id
        )
