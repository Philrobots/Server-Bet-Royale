

from datetime import datetime
from main.domain.identifiers.DomainId import DomainId
from main.domain.currency.Currency import Currency
from main.domain.transaction.TransactionType import TransactionType
from main.domain.sports_game.SportsGame import SportsGame

class TransactionInfo:
    def __init__(self, transaction_id:DomainId, user_id:DomainId, amount:Currency, transaction_type:TransactionType, date_created:datetime, current_balance:Currency, sports_game:SportsGame) -> None:
        self.transaction_id = transaction_id
        self.user_id = user_id
        self.amount = amount
        self.transaction_type = transaction_type
        self.date_created = date_created
        self.current_balance = current_balance
        self.sports_game = sports_game