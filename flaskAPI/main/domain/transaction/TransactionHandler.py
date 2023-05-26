from main.domain.transaction.TransactionFactory import TransactionFactory
from main.domain.identifiers.DomainId import DomainId
from main.domain.currency.Currency import Currency
from main.domain.transaction.TransactionType import TransactionType
from main.infra.db.repository.TransactionRepository import TransactionRepository

class TransactionHandler:
    
    def __init__(self, transaction_repository: TransactionRepository):
        self.transaction_repository = transaction_repository
        
        
    def create_add_funds_transaction(self, user_id: DomainId, amount: Currency, current_balance: Currency):
        transaction = TransactionFactory.create(
            user_id,
            amount,
            TransactionType.ADD_FUNDS,
            bet_id=None,
            current_balance=current_balance
        )
        
        self.transaction_repository.add_transaction(transaction)

    def create_retrieve_funds_transaction(self, user_id: DomainId, amount: Currency, current_balance: Currency):
        transaction = TransactionFactory.create(
            user_id,
            amount,
            TransactionType.RETRIEVE_FUNDS,
            bet_id=None,
            current_balance=current_balance
        )
        
        self.transaction_repository.add_transaction(transaction)

    def create_created_bet_transaction(self, user_id: DomainId, amount:Currency, bet_id: DomainId, current_balance: Currency):
        transaction = TransactionFactory.create(
            user_id,
            amount=amount,
            transaction_type=TransactionType.CREATE_BET,
            bet_id=bet_id,
            current_balance=current_balance
        )
        
        self.transaction_repository.add_transaction(transaction)

    def create_accepted_bet_transaction(self, user_id: DomainId, amount:Currency, bet_id: DomainId, current_balance: Currency):
        transaction = TransactionFactory.create(
            user_id,
            amount=amount,
            transaction_type=TransactionType.ACCEPT_BET,
            bet_id=bet_id,
            current_balance=current_balance
        )
        
        self.transaction_repository.add_transaction(transaction)

    def create_won_bet_transaction(self, user_id:DomainId, amount:Currency, bet_id: DomainId, current_balance: Currency):
        transaction = TransactionFactory.create(
            user_id,
            amount=amount,
            transaction_type=TransactionType.WON_BET,
            bet_id=bet_id,
            current_balance=current_balance
        )
        
        self.transaction_repository.add_transaction(transaction)

    def create_lost_bet_transaction(self, user_id: DomainId, bet_id: DomainId, current_balance:Currency):
        transaction = TransactionFactory.create(
            user_id,
            amount=None,
            transaction_type=TransactionType.LOST_BET,
            bet_id=bet_id,
            current_balance=current_balance
        )
        
        self.transaction_repository.add_transaction(transaction)

    def create_refund_transaction(self, user_id: DomainId, bet_id: DomainId, amount: Currency, current_balance: Currency):
        transaction = TransactionFactory.create(
            user_id,
            amount=amount,
            transaction_type=TransactionType.REFUND,
            bet_id=bet_id,
            current_balance=current_balance
        )
        
        self.transaction_repository.add_transaction(transaction)