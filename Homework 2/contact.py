"""
Course: PROG 1403 – Programming Logic 2
Semester: Spring 2026
Project: HW2 – Contact List
Author: Rakshith Jayakarthikeyan
"""

from __future__ import annotations
from dataclasses import dataclass
from datetime import date


@dataclass(order=True)
class Contact:
    # Sorted by last_name, then first_name (both stored lowercase)
    last_name: str
    first_name: str
    birthday: date

    def display_last(self) -> str:
        return self.last_name.title()

    def display_first(self) -> str:
        return self.first_name.title()

    def birthday_iso(self) -> str:
        return self.birthday.isoformat()

    def age_current_year(self) -> int:
        # Requirement: calculate age based on current year (no hard-code)
        return date.today().year - self.birthday.year