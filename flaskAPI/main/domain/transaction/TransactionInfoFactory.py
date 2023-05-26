
from typing import List
from main.domain.currency.Currency import Currency
from main.domain.exception.InvalidLostBetTransaction import InvalidLostBetTransaction
from main.domain.transaction.Transaction import Transaction
from main.domain.transaction.TransactionInfo import TransactionInfo
from main.domain.transaction.TransactionType import TransactionType
from main.infra.db.repository.BetRepository import BetRepository


class TransactionInfoFactory:
    def __init__(self, bet_repository: BetRepository):
        self.bet_repository = bet_repository

    def create_all(self, transactions: List[Transaction]) -> List[TransactionInfo]:
        return_list = []
        for transaction in transactions:
            if transaction.transaction_type == TransactionType.WON_BET:
                return_list.append(self._create_one_won_transaction(transaction))
            elif transaction.transaction_type == TransactionType.LOST_BET:

                corresponding_transaction = next((item for item in transactions if item.bet_id == transaction.bet_id
                                                  and item.transaction_type in (TransactionType.ACCEPT_BET, TransactionType.CREATE_BET)), None)

                if (corresponding_transaction is None or corresponding_transaction.amount is None):
                    raise InvalidLostBetTransaction

                return_list.append(self._create_one_lost_transaction(transaction, corresponding_transaction.amount))
        return return_list

    def _create_one_won_transaction(self, transaction: Transaction) -> TransactionInfo:
        bet = self.bet_repository.get_by_id(transaction.bet_id)
        sports_game = bet.sports_game
        return TransactionInfo(transaction.transaction_id, transaction.user_id, bet.get_won_amount(transaction.user_id),
                               transaction.transaction_type, transaction.date_created, transaction.current_balance,
                                sports_game)
    
    def _create_one_lost_transaction(self, transaction:Transaction, amount:Currency) -> TransactionInfo:
        bet = self.bet_repository.get_by_id(transaction.bet_id)
        sports_game = bet.sports_game
        return TransactionInfo(transaction.transaction_id, transaction.user_id, amount,
                               transaction.transaction_type, transaction.date_created, transaction.current_balance,
                                sports_game)
