"""
Course: PROG 1403 – Programming Logic 2
Semester: Spring 2026
Project: HW2 – Contact List
Author: Rakshith Jayakarthikeyan
"""

import sys
from datetime import date, datetime
from pathlib import Path
import csv
from contact import Contact


FILE_NAME = Path(__file__).resolve().parent / "Contacts.csv"
contacts = []


def print_menu():
    print("1. Enter a new Contact from the console")
    print("2. Import Contacts from a file")
    print("3. Display all Contacts on the console")
    print("4. Export all Contacts to a file")
    print("5. Delete a single Contact")
    print("6. Exit")


def parse_date(text):
    text = text.strip()
    if not text:
        return None

    for fmt in ("%m/%d/%Y", "%m/%d/%y", "%Y-%m-%d"):
        try:
            parsed = datetime.strptime(text, fmt).date()
            if 1800 <= parsed.year <= 2200:
                return parsed
            return None
        except ValueError:
            continue

    if "/" in text:
        try:
            month, day = [int(part) for part in text.split("/")]
            return date(2026, month, day)
        except (ValueError, TypeError):
            return None

    return None


def add_contact():
    first = input("Enter first name: ").strip()
    last = input("Enter last name: ").strip()

    if not first or not last:
        print("Invalid name.")
        return

    birthday = None
    while birthday is None:
        birthday = parse_date(input("Enter birthday (m/d/y, m/d, or y-m-d): "))
        if birthday is None:
            print("Invalid date. Try again.")

    contacts.append(Contact(last, first, birthday))
    contacts.sort(key=lambda c: (c.last_name, c.first_name))
    print("Contact added.")


def display_contacts():
    if not contacts:
        print("No contacts.")
        return

    print(f"{'Last Name, First Name':<28} {'Birthdate':<14} {'Age':>3}")
    for contact in contacts:
        print(
            f"{contact.get_display_name():<28} "
            f"{contact.get_birthdate_str():<14} "
            f"{contact.get_age():>3}"
        )


def import_contacts():
    try:
        with open(FILE_NAME, newline="") as csv_file:
            for row in csv.reader(csv_file):
                if len(row) < 3:
                    continue
                first, last, birthday = row[:3]
                parsed_date = parse_date(birthday)
                if parsed_date:
                    contacts.append(Contact(last.strip(), first.strip(), parsed_date))
        contacts.sort(key=lambda c: (c.last_name, c.first_name))
        print("Contacts imported.")
    except Exception:
        print("Import failed.")


def export_contacts():
    try:
        with open(FILE_NAME, "w", newline="") as csv_file:
            writer = csv.writer(csv_file)
            for contact in contacts:
                writer.writerow(
                    [contact.first_name, contact.last_name, contact.get_birthdate_str()]
                )
        print("Contacts exported.")
    except Exception:
        print("Export failed.")


def delete_contact():
    first = input("Enter first name to delete: ").strip().lower()
    last = input("Enter last name to delete: ").strip().lower()

    for contact in contacts:
        if contact.first_name == first and contact.last_name == last:
            contacts.remove(contact)
            print("Contact deleted.")
            return
    print("Contact not found.")


def main():
    print("HW2 – Contact List")
    print("Solution by Rakshith Jayakarthikeyan")
    print()

    actions = {
        "1": add_contact,
        "2": import_contacts,
        "3": display_contacts,
        "4": export_contacts,
        "5": delete_contact,
    }

    while True:
        print_menu()
        choice = input("Enter choice: ").strip()
        print()

        if choice == "6":
            print("HW2 Complete")
            break

        action = actions.get(choice)
        if action:
            action()
        else:
            print("Invalid choice.")

        print()


if __name__ == "__main__":
    main()
