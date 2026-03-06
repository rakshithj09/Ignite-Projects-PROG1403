from sales import Sales


class Displayable:
    def get_name_fields(self):
        raise NotImplementedError

    def get_annual_value(self):
        raise NotImplementedError

    def get_monthly_values(self):
        raise NotImplementedError


class Model(Displayable):
    def __init__(self, brand_name, model_name, sales):
        self.brand_name = brand_name.strip()
        self.model_name = model_name.strip()
        self.sales = sales

    def get_name_fields(self):
        return (self.brand_name, self.model_name)

    def get_annual_value(self):
        return self.sales.annual_total()

    def get_monthly_values(self):
        return self.sales.monthly()
