

from main.domain.better_stats.BetterStats import BetterStats
from main.domain.better_stats.BetterStatsFactory import BetterStatsFactory
from main.domain.identifiers.DomainId import DomainId
from main.infra.db.repository.TransactionRepository import TransactionRepository


class BetterStatsService:
    def __init__(self, transaction_repository: TransactionRepository, better_stats_factory: BetterStatsFactory):
        self.transaction_repository = transaction_repository
        self.better_stats_factory = better_stats_factory

    def calculate_better_stats(self, better_id: DomainId) -> BetterStats:
        transactions = self.transaction_repository.get_transactions(better_id)
        return self.better_stats_factory.create(transactions)
    
    def remove_old_transactions(self) -> int:
        return self.transaction_repository.remove_old_transactions()
