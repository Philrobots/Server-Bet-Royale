


class Currency:

    def __init__(self, amount: float, currency_str: str = "CAD"):
        self.amount = amount
        self.currency_str = currency_str

    def __add__(self, other: "Currency"):
        return Currency(self.amount + other.amount)

    def __hash__(self):
        return hash(self.amount)

    def __eq__(self, other: "Currency"):
        return self.amount == other.amount

    def __neq__(self, other: "Currency"):
        return self.amount != other.amount

    def __mul__(self, times:float):
        return Currency(self.amount * times)

    def __truediv__(self, denominator:float):
        return Currency(self.amount / denominator)

    def __float__(self):
        return float(self.amount)

    def __sub__(self, other: "Currency"):
        return Currency(self.amount - other.amount)

    def __isub__(self, other: "Currency"):
        self.amount -= other.amount
        return self

    def __iadd__(self, other: "Currency"):
        self.amount += other.amount
        return self

    def __gt__(self, other: "Currency"):
        return self.amount > other.amount

    def __round__(self, n=None):
        return Currency(round(self.amount, n))

    def __neg__(self):
        return Currency(-self.amount)
    
    def __ge__(self, other: "Currency"):
        return self.amount >= other.amount
