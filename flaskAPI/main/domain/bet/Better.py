from ctypes import Array
from main.domain.currency.Currency import Currency
from main.domain.exception.NotEnoughFundInBankException import NotEnoughFundInBankException
from main.domain.identifiers.DomainId import DomainId
from datetime import datetime
from main.domain.transaction.TransactionHandler import TransactionHandler


class Better:

    def __init__(self, user_id: DomainId, birth_date: datetime, bank_balance:Currency, created_bet_ids: Array[DomainId], accepted_bet_ids: Array[DomainId], transaction_handler: TransactionHandler):
        self.user_id = user_id
        self.birth_date = birth_date
        self.bank_balance = bank_balance
        self.created_bet_ids = created_bet_ids
        self.accepted_bet_ids = accepted_bet_ids
        self.transaction_handler = transaction_handler
        self.won_bet_ids = []
        self.lost_bet_ids = []
        self.uncompleted_bet_ids = []

    def get_balance(self) -> float:
        return self.bank_balance

    def retrieve_amount(self, amount_to_retrieve: Currency):
        if self.verify_sufficient_funds(amount_to_retrieve):
            self.bank_balance -= amount_to_retrieve
            return

        raise NotEnoughFundInBankException

    def add_funds(self, amount_to_add: Currency):
        self.bank_balance += amount_to_add
        self.transaction_handler.create_add_funds_transaction(self.user_id, amount_to_add, self.bank_balance)

    def verify_sufficient_funds(self, amount: Currency) -> bool:
        return self.bank_balance >= amount

    def add_created_bet(self, bet_amount:Currency, bet_id: DomainId):
        self.created_bet_ids.append(bet_id)

        self.retrieve_amount(bet_amount)
        self.transaction_handler.create_created_bet_transaction(self.user_id, -bet_amount, bet_id, self.bank_balance)

    def add_accepted_bet(self, bet_amount:Currency, bet_id: DomainId):
        self.accepted_bet_ids.append(bet_id)

        self.retrieve_amount(bet_amount)
        self.transaction_handler.create_accepted_bet_transaction(self.user_id, -bet_amount, bet_id, self.bank_balance)


    def _remove_bet_from_created_or_accepted(self, bet_id: DomainId):
        if bet_id in self.created_bet_ids:
            self.created_bet_ids.remove(bet_id)
        if bet_id in self.accepted_bet_ids:
            self.accepted_bet_ids.remove(bet_id)

    def add_won_bet(self, payout:Currency, bet_id: DomainId):
        self.won_bet_ids.append(bet_id)

        self._remove_bet_from_created_or_accepted(bet_id)

        self.bank_balance += payout
        self.transaction_handler.create_won_bet_transaction(self.user_id, payout, bet_id, self.bank_balance)

    def add_lost_bet(self, bet_id: DomainId):
        self.lost_bet_ids.append(bet_id)

        self._remove_bet_from_created_or_accepted(bet_id)

        self.transaction_handler.create_lost_bet_transaction(self.user_id, bet_id, self.bank_balance)

    def add_uncompleted_bet(self, bet_amount:Currency, bet_id: DomainId):
        self.uncompleted_bet_ids.append(bet_id)

        self.created_bet_ids.remove(bet_id)

        self.bank_balance += bet_amount
        self.transaction_handler.create_refund_transaction(self.user_id, bet_id, bet_amount, self.bank_balance)

    def add_deleted_bet(self, bet_amount:Currency, bet_id: DomainId):
        self.created_bet_ids.remove(bet_id)

        self.bank_balance += bet_amount
        self.transaction_handler.create_refund_transaction(self.user_id, bet_id, bet_amount, self.bank_balance)