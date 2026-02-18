"""
Course: PROG 1403 – Programming Logic 2
Semester: Spring 2026
Project: HW1 – Counting Weekends
Author: Rakshith Jayakarthikeyan
"""

from datetime import date, timedelta


def parse_date(date_str):
    date_str = date_str.strip()

    try:
        if "/" in date_str:
            parts = date_str.split("/")
            if len(parts) == 3:
                month = int(parts[0])
                day = int(parts[1])
                year_part = parts[2]

                if len(year_part) == 2:
                    year = 2000 + int(year_part)
                else:
                    year = int(year_part)

            elif len(parts) == 2:
                month = int(parts[0])
                day = int(parts[1])
                year = 2026
            else:
                raise ValueError

        elif "-" in date_str:
            parts = date_str.split("-")

            if len(parts) != 3:
                raise ValueError

            year_part = parts[0]
            month = int(parts[1])
            day = int(parts[2])

            if len(year_part) == 2:
                year = 2000 + int(year_part)
            else:
                year = int(year_part)
        else:
            raise ValueError

        if year < 1800 or year > 2200:
            raise ValueError

        return date(year, month, day)

    except Exception:
        return None


def count_weekends(start_date, end_date):
    full = 0
    sat_only = 0
    sun_only = 0

    current = start_date

    while current <= end_date:
        if current.weekday() == 5:
            next_day = current + timedelta(days=1)

            if next_day <= end_date:
                full += 1
                current += timedelta(days=2)
            else:
                sat_only += 1
                current += timedelta(days=1)

        elif current.weekday() == 6:
            prev_day = current - timedelta(days=1)

            if prev_day < start_date:
                sun_only += 1

            current += timedelta(days=1)

        else:
            current += timedelta(days=1)

    total = full + sat_only + sun_only
    return full, sat_only, sun_only, total


def main():
    print("HW1 – Counting Weekends")
    print("Solution by YOUR FULL NAME")
    print()

    print("Dates must be entered as 'm/d/y', 'm/d', or 'y-m-d'.")
    print("In the 'm/d' format, the year defaults to 2026.")
    print()

    while True:
        start_date = None
        end_date = None

        while start_date is None:
            user_input = input("What is the starting date? ")
            start_date = parse_date(user_input)
            if start_date is None:
                print("Invalid date. Please try again.")

        while end_date is None:
            user_input = input("What is the ending date? ")
            end_date = parse_date(user_input)
            if end_date is None:
                print("Invalid date. Please try again.")

        if start_date > end_date:
            start_date, end_date = end_date, start_date

        print()
        print(f"startDate = {start_date}")
        print(f"startDate = {start_date.strftime('%A')}")
        print(f"endDate = {end_date}")
        print(f"endDate = {end_date.strftime('%A')}")
        print()

        full, sat_only, sun_only, total = count_weekends(start_date, end_date)

        print(f"Full Weekends: {full}")
        print(f"Saturday-only Weekends: {sat_only}")
        print(f"Sunday-only Weekends: {sun_only}")
        print(f"Total Weekends: {total}")
        print()

        again = input("Check another date range? (Y/N) ")
        if again.lower() != "y":
            break

        print()

    print("HW1 Complete")


if __name__ == "__main__":
    main()