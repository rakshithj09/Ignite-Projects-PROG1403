class Sales:
    MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
              "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

    def __init__(self, monthly=None):
        if monthly is None:
            self._monthly = [0] * 12
        else:
            if len(monthly) != 12:
                raise ValueError("Sales needs 12 monthly values.")
            self._monthly = [int(x) for x in monthly]

    def monthly(self):
        return list(self._monthly)

    def annual_total(self):
        return sum(self._monthly)

    def __add__(self, other):
        return Sales([a + b for a, b in zip(self._monthly, other._monthly)])
