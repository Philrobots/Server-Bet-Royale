

from marshmallow.fields import Field

from main.domain.currency.Currency import Currency


class NullableCurrencyField(Field):

    def _deserialize(self, amount: Currency | None, *args, **kwargs):
        return Currency(amount) if amount is not None else None

    def _serialize(self, value: Currency, *args, **kwargs):
        return float(value) if value is not None else None
