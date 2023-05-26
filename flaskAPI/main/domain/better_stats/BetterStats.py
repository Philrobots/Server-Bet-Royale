

from typing import List
from main.domain.transaction.TransactionInfo import TransactionInfo
from main.domain.transaction.TransactionType import TransactionType


class BetterStats:
    def __init__(self, transaction_infos: List[TransactionInfo]):
        self.wins = self._calculate_wins(transaction_infos)
        self.losses = self._calculate_losses(transaction_infos)
        self.win_rate = self._calculate_win_rate(self.wins, self.losses)
        self.transaction_infos = transaction_infos
        

    def _calculate_wins(self, transactions : List[TransactionInfo]) -> int:
        wins = 0
        for transaction in transactions:
            if transaction.transaction_type == TransactionType.WON_BET:
                wins += 1

        return wins

    def _calculate_losses(self, transactions : List[TransactionInfo]) -> int:
        losses = 0
        for transaction in transactions:
            if transaction.transaction_type == TransactionType.LOST_BET:
                losses += 1

        return losses

    def _calculate_win_rate(self, wins: int, losses: int) -> float:
        if wins == 0 and losses == 0:
            return 0

        return round(100 * (wins / (wins + losses)), 2)