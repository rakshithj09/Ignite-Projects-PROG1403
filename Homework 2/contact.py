from datetime import date


class Contact:
    def __init__(self, last_name, first_name, birthday):
        self.last_name = last_name.lower()
        self.first_name = first_name.lower()
        self.birthday = birthday

    def get_display_name(self):
        return f"{self.last_name.title()}, {self.first_name.title()}"

    def get_birthdate_str(self):
        return self.birthday.isoformat()

    def get_age(self):
        today = date.today()
        years = today.year - self.birthday.year
        if (today.month, today.day) < (self.birthday.month, self.birthday.day):
            years -= 1
        return years
