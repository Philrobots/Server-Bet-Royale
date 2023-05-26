import typing

from marshmallow.fields import Field

from main.domain.currency.Currency import Currency


class CurrencyField(Field):

    def _deserialize(self, amount: typing.Any, *args, **kwargs):
        return Currency(float(amount))

    def _serialize(self, value: Currency, *args, **kwargs):
        return float(value)
