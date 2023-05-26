from datetime import datetime

import pytz

from main.domain.exception.InvalidIsoDateFormatException import InvalidIsoDateFormatException


class DateTimeHelper:
    def create_datetime_from_iso(self, iso_date_string:str) -> datetime:
        try:
            return datetime.fromisoformat(iso_date_string.replace('Z', '+00:00'))
        except ValueError:
            raise InvalidIsoDateFormatException


    def join_aware_or_naive_datetime_for_now(self, date:datetime) -> datetime:
        return datetime.now() if date.tzinfo is None or date.tzinfo.utcoffset(date) is None else pytz.UTC.localize(datetime.now())
