"""
Course: PROG 1403 – Programming Logic 2
Semester: Spring 2026
Project: HW3 – Vehicle Sales
Author: Rakshith Jayakarthikeyan
"""

import os

from data_manager import DataManager
from display_utils import print_annual_table, print_monthly_table
from brand import Brand
from model import Displayable


DATA_FILE = os.path.join(os.path.dirname(__file__), "US Vehicle Model Sales by Month 2025.txt")


def read_menu_choice():
    while True:
        s = input("Select an action by its number: (0-5): ").strip()
        try:
            n = int(s)
        except Exception:
            print("Enter a whole number from 0 to 5: ")
            continue
        if 0 <= n <= 5:
            return n
        print("Enter a number from 0 to 5: ")


def print_menu():
    print("Choose an action from this list by its number: ")
    print("1 - Import Vehicle Sales Data")
    print("2 - Display annual Sales Data for all Brands")
    print("3 - Display monthly Sales Data for all Brands")
    print("4 - Display annual Sales Data by Model for one Brand")
    print("5 - Display monthly Sales Data by Model for one Brand")
    print("0 - Exit")


def choose_brand(dm):
    brands = dm.brands_sorted()
    if not brands:
        return None

    print("Select a brand from this list by name or number:")
    for i, brand in enumerate(brands, start=1):
        print(f"{i:>2} - {brand.name}")

    while True:
        raw = input("Choose a brand by entering its name or number: ").strip()
        if raw == "":
            print("Enter a brand name or a number from the list.")
            continue

        if raw.isdigit():
            idx = int(raw)
            if 1 <= idx <= len(brands):
                return brands[idx - 1]
            print("Number not in range.")
            continue

        lowered = raw.lower()
        for brand in brands:
            if brand.name.lower() == lowered:
                return brand

        print("Brand not found. Try again.")


def ensure_loaded(dm):
    if dm.is_loaded():
        return True
    print("Data not loaded. Use option 1 first")
    return False


def option_import(dm):
    ok, msg = dm.import_from_tsv(str(DATA_FILE))
    print(msg)


def option_annual_all(dm):
    show_all_brands(dm, "Annual Sales for All Brands", print_annual_table)


def option_monthly_all(dm):
    show_all_brands(dm, "Monthly Sales for All Brands", print_monthly_table)


def option_annual_one_brand(dm):
    show_one_brand(dm, "Annual Sales for All Models of one Brand", print_annual_table)


def option_monthly_one_brand(dm):
    show_one_brand(dm, "Monthly Sales for All Models of one Brand", print_monthly_table)


class _BrandTotal(Displayable):
    def __init__(self, brand):
        self._brand = brand

    def get_name_fields(self):
        return (self._brand.name, "Total")

    def get_annual_value(self):
        return self._brand.get_annual_value()

    def get_monthly_values(self):
        return self._brand.get_monthly_values()


def show_all_brands(dm, title, printer):
    if not ensure_loaded(dm):
        return
    printer(title, dm.brands_sorted())


def show_one_brand(dm, title, printer):
    if not ensure_loaded(dm):
        return
    brand = choose_brand(dm)
    if brand is None:
        print("No brands found.")
        return

    rows = brand.models()
    rows.sort(key=lambda m: m.model_name.lower())
    rows.append(_BrandTotal(brand))
    printer(title, rows)


def main():
    print("HW3 - Vehicle Sales")
    print("Solution by Rakshith Jayakarthikeyan")
    print()

    dm = DataManager()

    while True:
        print_menu()
        choice = read_menu_choice()
        print()

        if choice == 0:
            print("HW3 Complete")
            return

        if choice == 1:
            option_import(dm)
        elif choice == 2:
            option_annual_all(dm)
        elif choice == 3:
            option_monthly_all(dm)
        elif choice == 4:
            option_annual_one_brand(dm)
        elif choice == 5:
            option_monthly_one_brand(dm)

        print()


if __name__ == "__main__":
    main()
