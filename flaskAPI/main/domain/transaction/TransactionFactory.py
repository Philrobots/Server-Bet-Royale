from datetime import datetime
from main.domain.transaction.Transaction import Transaction
from main.domain.identifiers.DomainId import DomainId
from main.domain.currency.Currency import Currency
from main.domain.transaction.TransactionType import TransactionType

class TransactionFactory:
    
    @staticmethod
    def create(user_id: DomainId, amount: Currency | None, transaction_type: TransactionType, bet_id: DomainId | None,
               current_balance: Currency):
        transaction_id = DomainId()
        
        return Transaction(
            transaction_id,
            user_id,
            amount,
            transaction_type,
            bet_id,
            datetime.now(),
            current_balance
        )