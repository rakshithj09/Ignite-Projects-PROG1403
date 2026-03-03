from __future__ import annotations
from sales import Sales


class Displayable:
    def get_name_fields(self) -> tuple[str, str]:
        raise NotImplementedError

    def get_annual_value(self) -> int:
        raise NotImplementedError

    def get_monthly_values(self) -> list[int]:
        raise NotImplementedError


class Model(Displayable):
    def __init__(self, brand_name: str, model_name: str, sales: Sales):
        self.brand_name = brand_name.strip()
        self.model_name = model_name.strip()
        self.sales = sales

    def get_name_fields(self) -> tuple[str, str]:
        return (self.brand_name, self.model_name)

    def get_annual_value(self) -> int:
        return self.sales.annual_total()

    def get_monthly_values(self) -> list[int]:
        return self.sales.monthly()