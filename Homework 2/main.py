"""
Course: PROG 1403 – Programming Logic 2
Semester: Spring 2026
Project: HW2 – Contact List
Author: Rakshith Jayakarthikeyan
"""

from datetime import date, datetime
import csv
from contact import Contact

contacts = []
FILE_NAME = "Contacts.csv"


def print_menu():
    print("1. Enter a new Contact from the console")
    print("2. Import Contacts from a file")
    print("3. Display all Contacts on the console")
    print("4. Export all Contacts to a file")
    print("5. Delete a single Contact")
    print("6. Exit")


def parse_date(text):
    try:
        if "/" in text:
            parts = text.split("/")
            if len(parts) == 3:
                month = int(parts[0])
                day = int(parts[1])
                year = int(parts[2])
                if year < 100:
                    year += 2000
            elif len(parts) == 2:
                month = int(parts[0])
                day = int(parts[1])
                year = 2026
            else:
                return None

        elif "-" in text:
            parts = text.split("-")
            if len(parts) != 3:
                return None
            year = int(parts[0])
            month = int(parts[1])
            day = int(parts[2])

        else:
            return None

        if year < 1800 or year > 2200:
            return None

        return date(year, month, day)

    except:
        return None


def sort_contacts():
    contacts.sort(key = lambda c: (c.last_name, c.first_name))


def add_contact():
    first = input("Enter first name: ").strip()
    last = input("Enter last name: ").strip()

    if first == "" or last == "":
        print("Invalid name.")
        return

    bday = None
    while bday is None:
        raw = input("Enter birthday (m/d/y, m/d, or y-m-d): ")
        bday = parse_date(raw)
        if bday is None:
            print("Invalid date. Try again.")

    contacts.append(Contact(last, first, bday))
    sort_contacts()
    print("Contact added.")


def display_contacts():
    if len(contacts) == 0:
        print("No contacts.")
        return

    print(f"{'Last Name, First Name':<28} {'Birthdate':<14} {'Age':>3}")

    for c in contacts:
        print(f"{c.get_display_name():<28} {c.get_birthdate_str():<14} {c.get_age():>3}")


def import_contacts():
    try:
        with open(FILE_NAME, newline="") as f:
            reader = csv.reader(f)
            for row in reader:
                first = row[0].strip()
                last = row[1].strip()
                bday = parse_date(row[2].strip())
                if bday:
                    contacts.append(Contact(last, first, bday))

        sort_contacts()
        print("Contacts imported.")

    except:
        print("Import failed.")


def export_contacts():
    try:
        with open(FILE_NAME, "w", newline = "") as f:
            writer = csv.writer(f)
            for c in contacts:
                writer.writerow([c.first_name, c.last_name, c.get_birthdate_str()])
        print("Contacts exported.")

    except:
        print("Export failed.")


def delete_contact():
    first = input("Enter first name to delete: ").strip().lower()
    last = input("Enter last name to delete: ").strip().lower()

    for c in contacts:
        if c.first_name == first and c.last_name == last:
            contacts.remove(c)
            print("Contact deleted.")
            return

    print("Contact not found.")


def main():
    print("HW2 – Contact List")
    print("Solution by Rakshith Jayakarthikeyan")
    print()

    while True:
        print_menu()
        choice = input("Enter choice: ").strip()
        print()

        if choice == "1":
            add_contact()
        elif choice == "2":
            import_contacts()
        elif choice == "3":
            display_contacts()
        elif choice == "4":
            export_contacts()
        elif choice == "5":
            delete_contact()
        elif choice == "6":
            print("HW2 Complete")
            break
        else:
            print("Invalid choice.")

        print()


if __name__ == "__main__":
    main()