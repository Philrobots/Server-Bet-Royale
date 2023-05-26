
from main.infra.db.repository.BetRepository import BetRepository
from main.infra.db.repository.BetterRepository import BetterRepository
from main.service.BetService import BetService


class BetScheduler:
    def __init__(self, bet_service:BetService, bet_repo:BetRepository, better_repo:BetterRepository):
        self.bet_service = bet_service
        self.bet_repo = bet_repo
        self.better_repo = better_repo

    def complete_bets(self):
        all_completable_bets = self.bet_repo.get_completable_bets()
        for bet in all_completable_bets:
            if bet.sports_game.is_completed() and not bet.is_completed:
                home_betters = [self.better_repo.get_by_id(better_id) for better_id in bet.get_home_better_ids()]
                away_betters = [self.better_repo.get_by_id(better_id) for better_id in bet.get_away_better_ids()]

                bet.complete_bet(home_betters, away_betters)
                self.bet_repo.update_bet(bet)
                for better in home_betters:
                    self.better_repo.update_better(better)
                for better in away_betters:
                    self.better_repo.update_better(better)