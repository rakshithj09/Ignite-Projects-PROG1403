from sales import Sales
from model import Model, Displayable


class Brand(Displayable):
    def __init__(self, name):
        self.name = name.strip()
        self._models = []

    def add_model(self, model):
        self._models.append(model)

    def models(self):
        return list(self._models)

    def aggregate_sales(self):
        return sum((m.sales for m in self._models), Sales())

    def get_name_fields(self):
        return (self.name, "")

    def get_annual_value(self):
        return self.aggregate_sales().annual_total()

    def get_monthly_values(self):
        return self.aggregate_sales().monthly()
