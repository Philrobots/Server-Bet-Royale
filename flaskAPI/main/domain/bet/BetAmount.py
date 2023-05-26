


from main.domain.currency.Currency import Currency
from main.domain.identifiers.DomainId import DomainId


class BetAmount:
    def __init__(self, id:DomainId, is_author:bool, better_id:DomainId, amount:Currency):
        self.id = id
        self.is_author = is_author
        self.better_id = better_id
        self.amount = amount