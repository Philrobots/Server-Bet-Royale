from datetime import datetime
from main.domain.identifiers.DomainId import DomainId
from main.domain.currency.Currency import Currency
from main.domain.transaction.TransactionType import TransactionType

class Transaction:
    
    def __init__(self, transaction_id: DomainId, user_id: DomainId, amount: Currency | None,
                 transaction_type: TransactionType, bet_id: DomainId | None, date_created: datetime,
                 current_balance: Currency):
        self.transaction_id = transaction_id
        self.user_id = user_id
        self.amount = amount
        self.transaction_type = transaction_type
        self.bet_id = bet_id
        self.date_created = date_created
        self.current_balance = current_balance
        