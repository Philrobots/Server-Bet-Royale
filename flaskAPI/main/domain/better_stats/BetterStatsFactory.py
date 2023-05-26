

from typing import List
from main.domain.better_stats.BetterStats import BetterStats

from main.domain.transaction.Transaction import Transaction
from main.domain.transaction.TransactionInfoFactory import TransactionInfoFactory


class BetterStatsFactory:
    def __init__(self, transaction_info_factory: TransactionInfoFactory):
        self.transaction_info_factory = transaction_info_factory

    def create(self, transactions: List[Transaction]):
        transaction_infos = self.transaction_info_factory.create_all(transactions)
        return BetterStats(transaction_infos)
