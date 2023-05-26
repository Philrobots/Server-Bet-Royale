

from main.domain.currency.Currency import Currency
from main.domain.exception.InvalidNumericalOddsException import InvalidNumericalOddsException
from main.domain.odds.Odds import Odds


class OddsFactory:
    @staticmethod
    def create(odds:float, is_home_odds:bool, bet_amount:Currency):
        if odds <= 1:
            raise InvalidNumericalOddsException
        return Odds(odds, is_home_odds, bet_amount)