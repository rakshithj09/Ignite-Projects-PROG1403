from datetime import date


class Contact:
    def __init__(self, last_name, first_name, birthday, phone = ""):
        self.last_name = last_name.strip().lower()
        self.first_name = first_name.strip().lower()
        self.birthday = birthday  # a datetime.date or None
        # Store phone as plain string, keep only digits (up to 15)
        self.phone = "".join(c for c in phone if c.isdigit())[:15]

    def get_display_name(self):
        return f"{self.last_name.title()}, {self.first_name.title()}"

    def get_birthdate_str(self):
        return self.birthday.isoformat() if self.birthday else ""

    def get_age(self):
        if not self.birthday:
            return ""
        today = date.today()
        years = today.year - self.birthday.year
        if (today.month, today.day) < (self.birthday.month, self.birthday.day):
            years -= 1
        return years

    def phone_str(self):
        # Format phone: +c (aaa) nnn-nnnn for 10+ digits, else plain
        d = self.phone
        if not d:
            return ""
        if len(d) >= 10:
            country = d[:-10] or "1"
            area = d[-10:-7]
            n1 = d[-7:-4]
            n2 = d[-4:]
            return f"+{country} ({area}) {n1}-{n2}"
        if len(d) > 4:
            return f"{d[:-4]}-{d[-4:]}"
        return d

    def key(self):
        return (self.last_name, self.first_name)
