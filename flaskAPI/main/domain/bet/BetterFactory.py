from dateutil.relativedelta import relativedelta
from main.domain.date.DateTimeHelper import DateTimeHelper
from main.domain.exception.InvalidBirthDateException import InvalidBirthDateException
from main.domain.bet.Better import Better
from main.domain.currency.Currency import Currency

from main.domain.exception.InvalidIsoDateFormatException import InvalidIsoDateFormatException
from main.domain.transaction.TransactionHandler import TransactionHandler


class BetterFactory:
    def __init__(self, date_time_helper:DateTimeHelper, transaction_handler: TransactionHandler):
        self.date_time_helper = date_time_helper
        self.transaction_handler = transaction_handler

    def create(self, user_id, birth_date):
        initial_balance = Currency(0)
        better = Better(user_id, self._validate_birth_date(birth_date), initial_balance, created_bet_ids=[], accepted_bet_ids=[], transaction_handler=self.transaction_handler)
        better.add_funds(Currency(1000))
        return better

    def _validate_birth_date(self, birth_date):
        try:
            datetime_birthdate = self.date_time_helper.create_datetime_from_iso(birth_date)
        except InvalidIsoDateFormatException:
            raise InvalidBirthDateException

        now = self.date_time_helper.join_aware_or_naive_datetime_for_now(datetime_birthdate)

        difference = relativedelta(now, datetime_birthdate)

        if difference.years < 18:
            raise InvalidBirthDateException

        return datetime_birthdate
