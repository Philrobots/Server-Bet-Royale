
from typing import List
from main.domain.bet.AcceptBetInfo import AcceptBetInfo
from main.domain.bet.Bet import Bet
from main.domain.bet.BetFactory import BetFactory
from main.domain.currency.Currency import Currency
from main.domain.identifiers.DomainId import DomainId
from main.infra.db.repository.BetRepository import BetRepository
from main.infra.db.repository.BetterRepository import BetterRepository
from main.infra.db.repository.SportsGameRepository import SportsGameRepository
from main.domain.bet.BetAmountFactory import BetAmountFactory

class BetService:

    def __init__(self, better_repo:BetterRepository, sports_game_repo:SportsGameRepository, bet_factory:BetFactory, bet_repo: BetRepository,
                 bet_amount_factory: BetAmountFactory):
        self.better_repo = better_repo
        self.sports_game_repo = sports_game_repo
        self.bet_factory = bet_factory
        self.bet_repo = bet_repo
        self.bet_amount_factory = bet_amount_factory


    def create_bet(self, sports_game_id: DomainId, better_id:DomainId, bet_amount_currency:Currency, odds:float, is_home_bet:bool):
        better = self.better_repo.get_by_id(better_id)
        better.verify_sufficient_funds(bet_amount_currency)

        sports_game = self.sports_game_repo.get_by_id(sports_game_id)
        sports_game.verify_completed_for_bet_creation()

        bet = self.bet_factory.create(better_id, sports_game, bet_amount_currency, odds, is_home_bet)
        better.add_created_bet(bet.get_created_bet_amount(), bet.id)

        self.better_repo.update_better(better)

        self.bet_repo.add_bet(bet)
    
    def get_accepted_bet(self, better_id: DomainId)-> List[Bet]:
        better = self.better_repo.get_by_id(better_id)
        bet_ids = better.accepted_bet_ids
        bets = []
        for i in bet_ids:
            bet = self.bet_repo.get_by_id(i)
            bets.append(bet)
            
        return bets

    def get_all_bets(self)-> List[Bet]:
        return self.bet_repo.get_all()
    
    def get_open_bets(self)-> List[Bet]:
        return self.bet_repo.get_open_bet()
    
    def get_user_open_bets(self, user_id: DomainId)-> List[Bet]:
        return self.bet_repo.get_user_open_bet(user_id)
    
    def get_user_active_bet(self, user_id: DomainId) -> List[Bet]:
        accepted_bet = self.get_accepted_bet(user_id)
        user_active_own_bet = self.bet_repo.get_user_active_bet(user_id)
        return accepted_bet + user_active_own_bet
    
    def accept_bet(self, accept_bet_info: AcceptBetInfo) -> Bet:
        
        bet = self.bet_repo.get_by_id(accept_bet_info.bet_id)
        better = self.better_repo.get_by_id(accept_bet_info.user_id)
        better.verify_sufficient_funds(bet.get_missing_amount())
        
        bet.accept_bet(accept_bet_info, self.bet_amount_factory)
        better.add_accepted_bet(bet.get_accepted_bet_amount(), bet.id)
        
        self.bet_repo.update_bet(bet)
        self.better_repo.update_better(better)
    
        return bet

    def delete_bet(self, bet_id:DomainId, user_id:DomainId):
        bet = self.bet_repo.get_by_id(bet_id)
        better = self.better_repo.get_by_id(user_id)
        bet.delete_bet(better)
        self.bet_repo.delete_bet(bet.id)
        self.better_repo.update_better(better)