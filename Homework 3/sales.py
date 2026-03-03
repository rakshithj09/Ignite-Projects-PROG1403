from __future__ import annotations


class Sales:
    MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
              "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

    def __init__(self, monthly: list[int] | None = None):
        if monthly is None:
            self._monthly = [0] * 12
        else:
            if len(monthly) != 12:
                raise ValueError("Sales needs 12 monthly values.")
            self._monthly = [int(x) for x in monthly]

    def monthly(self) -> list[int]:
        return list(self._monthly)

    def annual_total(self) -> int:
        return sum(self._monthly)

    def add(self, other: "Sales") -> "Sales":
        return Sales([a + b for a, b in zip(self._monthly, other._monthly)])

    def __add__(self, other: "Sales") -> "Sales":
        return self.add(other)