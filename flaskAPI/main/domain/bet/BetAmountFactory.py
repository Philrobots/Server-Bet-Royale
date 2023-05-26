




from main.domain.bet.BetAmount import BetAmount
from main.domain.currency.Currency import Currency
from main.domain.identifiers.DomainId import DomainId


class BetAmountFactory:
    def create(self, is_author:bool, better_id:DomainId,  bet_amount_currency: Currency):
        return BetAmount(DomainId(), is_author, better_id, bet_amount_currency)