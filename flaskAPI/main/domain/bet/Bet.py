from ctypes import Array
from main.domain.bet.BetAmount import BetAmount
from main.domain.bet.Better import Better
from main.domain.currency.Currency import Currency
from main.domain.exception import BetCannotBeDeletedException
from main.domain.exception.BetAlreadyAcceptedException import BetAlreadyAcceptedException
from main.domain.exception.BetAlreadyCompletedException import BetAlreadyCompletedException
from main.domain.exception.BetAuthorAcceptedBetException import BetAuthorAcceptedBetException
from main.domain.exception.NoOpponentIdException import NoOpponentIdException
from main.domain.exception.UnableToGetBetAmountException import UnableToGetBetAmountException
from main.domain.identifiers.DomainId import DomainId
from main.domain.odds.Odds import Odds
from main.domain.sports_game.SportsGame import SportsGame
from main.domain.bet.AcceptBetInfo import AcceptBetInfo
from main.domain.bet.BetAmountFactory import BetAmountFactory

class Bet:

    def __init__(self, id: DomainId, sports_game:SportsGame, odds:Odds,
                 bet_amounts_home:Array[BetAmount], bet_amounts_away:Array[BetAmount], is_completed:bool, 
                 is_home_bet:bool, is_accepted: bool, owner_id: DomainId):
        self.id = id
        self.sports_game = sports_game
        self.odds = odds
        self.bet_amounts_home = bet_amounts_home
        self.bet_amounts_away = bet_amounts_away
        self.is_completed = is_completed
        self.is_home_bet = is_home_bet
        self.is_accepted = is_accepted
        self.owner_id = owner_id
        
    def get_owner_id(self)-> str:
        return self.owner_id.to_string()

    def get_opponent_id(self) -> DomainId:
        for bet_amount in self.bet_amounts_home:
            if bet_amount.better_id != self.owner_id:
                return bet_amount.better_id
        for bet_amount in self.bet_amounts_away:
            if bet_amount.better_id != self.owner_id:
                return bet_amount.better_id

        raise NoOpponentIdException

    def get_won_amount(self, user_id: DomainId) -> Currency:
        won_amount = Currency(0)
        for bet_amount in self.bet_amounts_home:
            if bet_amount.better_id != user_id:
                won_amount += bet_amount.amount

        for bet_amount in self.bet_amounts_away:
            if bet_amount.better_id != user_id:
                won_amount += bet_amount.amount

        return won_amount

    def get_created_bet_amount(self) -> Currency:
        for bet_amount in self.bet_amounts_home:
            if bet_amount.is_author:
                return bet_amount.amount
        for bet_amount in self.bet_amounts_away:
            if bet_amount.is_author:
                return bet_amount.amount
        raise UnableToGetBetAmountException

    def get_accepted_bet_amount(self) -> Currency:
        for bet_amount in self.bet_amounts_home:
            if not bet_amount.is_author:
                return bet_amount.amount
        for bet_amount in self.bet_amounts_away:
            if not bet_amount.is_author:
                return bet_amount.amount
        raise UnableToGetBetAmountException

    def get_missing_amount(self) -> Currency:
        return self.odds.get_missing_amount()
    
    def delete_bet(self, bet_owner:Better): 
        if self.is_accepted or self.is_completed or self.owner_id != bet_owner.user_id:
            raise BetCannotBeDeletedException
        
        bet_owner.add_deleted_bet(self.get_created_bet_amount(), self.id)

    def accept_bet(self, accept_bet_info: AcceptBetInfo, bet_amount_factory: BetAmountFactory):
        if self.is_accepted:
            raise BetAlreadyAcceptedException

        if self.owner_id == accept_bet_info.user_id:
            raise BetAuthorAcceptedBetException

        bet_amount = bet_amount_factory.create(is_author=False, better_id=accept_bet_info.user_id, bet_amount_currency=self.odds.get_missing_amount())
        
        if self.is_home_bet:
            self.bet_amounts_away.append(bet_amount)
        else:
            self.bet_amounts_home.append(bet_amount)
        
        self.is_accepted = True
        self.odds.clear_missing_amounts()
        

    def get_home_better_ids(self) -> Array[DomainId]:
        better_ids = set()
        for bet_amount in self.bet_amounts_home:
            better_ids.add(bet_amount.better_id)
        return list(better_ids)

    def get_away_better_ids(self) -> Array[DomainId]:
        better_ids = set()
        for bet_amount in self.bet_amounts_away:
            better_ids.add(bet_amount.better_id)
        return list(better_ids)

    def complete_bet(self, home_betters: Array[Better], away_betters: Array[Better]):
        if self.is_completed:
            raise BetAlreadyCompletedException

        if not self.is_accepted:
            self.is_completed = True
            for home_better in home_betters:
                if home_better.user_id == self.owner_id:
                    home_better.add_uncompleted_bet(self.get_created_bet_amount(), self.id)
                    return

            for away_better in away_betters:
                if away_better.user_id == self.owner_id:
                    away_better.add_uncompleted_bet(self.get_created_bet_amount(), self.id)
                    return
            return


        if self.sports_game.home_wins():
            for home_better in home_betters:
                home_better.add_won_bet(self.odds.payout, self.id)
            for away_better in away_betters:
                away_better.add_lost_bet(self.id)
        else:
            for home_better in home_betters:
                home_better.add_lost_bet(self.id)
            for away_better in away_betters:
                away_better.add_won_bet(self.odds.payout, self.id)

        self.is_completed = True