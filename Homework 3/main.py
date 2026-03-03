"""
Course: PROG 1403 – Programming Logic 2
Semester: Spring 2026
Project: HW3 – Vehicle Sales
Author: Rakshith Jayakarthikeyan
"""

from __future__ import annotations

from data_manager import DataManager
from display_utils import print_annual_table, print_monthly_table
from brand import Brand
from model import Model


def read_menu_choice() -> int:
    while True:
        s = input("Select an action by its number: (0-5) ").strip()
        try:
            n = int(s)
        except Exception:
            print("Enter a whole number from 0 to 5.")
            continue
        if 0 <= n <= 5:
            return n
        print("Enter a number from 0 to 5.")


def print_menu() -> None:
    print("Choose an action from this list by its number:")
    print("1 - Import Vehicle Sales Data")
    print("2 - Display annual Sales Data for all Brands")
    print("3 - Display monthly Sales Data for all Brands")
    print("4 - Display annual Sales Data by Model for one Brand")
    print("5 - Display monthly Sales Data by Model for one Brand")
    print("0 - Exit")


def choose_brand(dm: DataManager) -> Brand | None:
    brands = dm.brands_sorted()
    if not brands:
        return None

    print("Select a brand from this list by name or number:")
    for i, b in enumerate(brands, start=1):
        print(f"{i:>2} - {b.name}")

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

        for b in brands:
            if b.name.lower() == raw.lower():
                return b

        print("Brand not found. Try again.")


def ensure_loaded(dm: DataManager) -> bool:
    if dm.is_loaded():
        return True
    print("Data not loaded. Use option 1 first.")
    return False


def option_import(dm: DataManager) -> None:
    import os

    filename = "US Vehicle Model Sales by Month 2025.txt"
    base_dir = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(base_dir, filename)

    ok, msg = dm.import_from_tsv(path)
    print(msg)


def option_annual_all(dm: DataManager) -> None:
    if not ensure_loaded(dm):
        return
    rows = dm.brands_sorted()
    print_annual_table("Annual Sales for All Brands", rows)


def option_monthly_all(dm: DataManager) -> None:
    if not ensure_loaded(dm):
        return
    rows = dm.brands_sorted()
    print_monthly_table("Monthly Sales for All Brands", rows)


def option_annual_one_brand(dm: DataManager) -> None:
    if not ensure_loaded(dm):
        return
    brand = choose_brand(dm)
    if brand is None:
        print("No brands found.")
        return

    models = sorted(brand.models(), key=lambda m: m.model_name.lower())

    rows = []
    for m in models:
        rows.append(m)

    rows.append(_brand_total_as_displayable(brand))

    print_annual_table("Annual Sales for All Models of one Brand", rows)


def option_monthly_one_brand(dm: DataManager) -> None:
    if not ensure_loaded(dm):
        return
    brand = choose_brand(dm)
    if brand is None:
        print("No brands found.")
        return

    models = sorted(brand.models(), key=lambda m: m.model_name.lower())

    rows = []
    for m in models:
        rows.append(m)

    rows.append(_brand_total_as_displayable(brand))

    print_monthly_table("Monthly Sales for All Models of one Brand", rows)


def _brand_total_as_displayable(brand: Brand):
    class _TotalRow:
        def get_name_fields(self):
            return (brand.name, "Total")

        def get_annual_value(self):
            return brand.get_annual_value()

        def get_monthly_values(self):
            return brand.get_monthly_values()

    return _TotalRow()


def main() -> None:
    print("HW3 - Vehicle Sales")
    print("Solution by YOURNAME")
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