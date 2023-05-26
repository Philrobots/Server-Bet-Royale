from main.domain.currency.Currency import Currency
from multipledispatch import dispatch


class Odds:
    @dispatch(float, float, Currency, Currency, Currency)
    def __init__(self, home_odds:float, away_odds:float, payout:Currency, home_missing_amount:Currency, away_missing_amount: Currency):
        self.home_odds = home_odds
        self.away_odds = away_odds
        self.payout = payout
        self.home_missing_amount = home_missing_amount
        self.away_missing_amount = away_missing_amount

    @dispatch(float, bool, Currency)
    def __init__(self, odds:float, is_home_odds:bool, bet_amount:Currency):
        self.home_odds = odds if is_home_odds else self.calculate_inverse_odds(odds)
        self.away_odds = self.calculate_inverse_odds(odds) if is_home_odds else odds
        self.payout = self.calculate_payout(bet_amount, self.home_odds) if is_home_odds  else self.calculate_payout(bet_amount, self.away_odds)
        self.home_missing_amount =  Currency(0) if is_home_odds else self.calculate_missing_amount(self.payout, bet_amount)
        self.away_missing_amount = self.calculate_missing_amount(self.payout, bet_amount) if is_home_odds else Currency(0)
 
    def calculate_payout(self, bet_amount:Currency, odds:float) -> Currency:
        return round(bet_amount * odds, 2)

    def calculate_missing_amount(self, payout:Currency, bet_amount:Currency) -> Currency:
        return round(payout - bet_amount, 2)

    def calculate_inverse_odds(self, odds:float) -> float:
        return round(odds/(odds - 1), 2)

    def get_missing_amount(self) -> Currency:
        return self.home_missing_amount if self.home_missing_amount != Currency(0) else self.away_missing_amount

    def clear_missing_amounts(self):
        self.home_missing_amount = Currency(0)
        self.away_missing_amount = Currency(0)
