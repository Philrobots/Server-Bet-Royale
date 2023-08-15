
from main.domain.currency.Currency import Currency
from main.domain.identifiers.DomainId import DomainId
from main.infra.db.repository.BetterRepository import BetterRepository


class BetterFundsService:
    def __init__(self, better_repo: BetterRepository):
        self.better_repo = better_repo

    def get_balance(self, better_id: DomainId) -> Currency:
        better = self.better_repo.get_by_id(better_id)
        return better.get_balance()