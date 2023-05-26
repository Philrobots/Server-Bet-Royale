

from main.domain.bet.Bet import Bet
from main.domain.bet.BetAmountFactory import BetAmountFactory
from main.domain.currency.Currency import Currency
from main.domain.exception.BetAmountCannotBeNegativeOrZeroException import BetAmountCannotBeNegativeOrZeroException
from main.domain.identifiers.DomainId import DomainId
from main.domain.odds.OddsFactory import OddsFactory
from main.domain.sports_game.SportsGame import SportsGame


class BetFactory:
    def __init__(self, bet_amount_factory: BetAmountFactory):
        self.bet_amount_factory = bet_amount_factory

    def create(self, better_id: DomainId, sports_game: SportsGame, bet_amount_currency: Currency, numerical_odds: float, is_home_bet: bool) -> Bet:
        if bet_amount_currency.amount <= 0:
            raise BetAmountCannotBeNegativeOrZeroException

        bet_amount_array = [self.bet_amount_factory.create(
            True, better_id, bet_amount_currency)]

        odds = OddsFactory.create(
            numerical_odds, is_home_bet, bet_amount_currency)
        is_completed = False

        return Bet(DomainId(), sports_game, odds, bet_amount_array if is_home_bet else [], bet_amount_array if not is_home_bet else [],
                    is_completed, is_home_bet, is_accepted=False, owner_id=better_id)
