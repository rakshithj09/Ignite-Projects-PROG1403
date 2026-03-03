from __future__ import annotations
from sales import Sales
from model import Model, Displayable


class Brand(Displayable):
    def __init__(self, name: str):
        self.name = name.strip()
        self._models: list[Model] = []

    def add_model(self, model: Model) -> None:
        self._models.append(model)

    def models(self) -> list[Model]:
        return list(self._models)

    def aggregate_sales(self) -> Sales:
        total = Sales()
        for m in self._models:
            total = total + m.sales
        return total

    def get_name_fields(self) -> tuple[str, str]:
        return (self.name, "")

    def get_annual_value(self) -> int:
        return self.aggregate_sales().annual_total()

    def get_monthly_values(self) -> list[int]:
        return self.aggregate_sales().monthly()