"""
Course: PROG 1403 – Programming Logic 2
Semester: Spring 2026
Project: HW2 – Contact List
Author: Rakshith Jayakarthikeyan
"""

from datetime import date
import csv

from contact import Contact

CONTACTS_FILE = "Contacts.csv"


def print_header():
    print("HW2 – Contact List")
    print("Solution by Rakshith Jayakarthikeyan")
    print()


def menu_choice() -> str:
    print("1. Enter a new Contact from the console")
    print("2. Import Contacts from a file")
    print("3. Display all Contacts on the console")
    print("4. Export all Contacts to a file")
    print("5. Delete a single Contact")
    print("6. Exit")
    return input("Enter choice: ").strip()


def parse_date_hw1_rules(text: str) -> date | None:
    """
    TODO: Reuse the same date validation rules as HW1.
    Supported formats:
    - m/d/y (2 or 4 digit year, 2 digit year means 2000-2099)
    - m/d (year defaults to 2026)
    - y-m-d
    Valid years 1800 to 2200 inclusive.
    Return date object, or None if invalid.
    """
    return None


def insert_sorted(contacts: list[Contact], c: Contact) -> None:
    contacts.append(c)
    contacts.sort()  # Contact ordering comes from dataclass(order=True)


def input_contact() -> Contact | None:
    first = input("Enter first name: ").strip().lower()
    last = input("Enter last name: ").strip().lower()

    bday = None
    while bday is None:
        raw = input("Enter birthday (m/d/y, m/d, or y-m-d): ").strip()
        bday = parse_date_hw1_rules(raw)
        if bday is None:
            print("Invalid date. Try again.")

    if first == "" or last == "":
        print("Name fields cannot be blank.")
        return None

    return Contact(last_name=last, first_name=first, birthday=bday)


def import_contacts(contacts: list[Contact]) -> None:
    """
    Reads CONTACTS_FILE and creates Contact objects.
    CSV format expectation for students:
    TODO: match whatever format instructor provided.
    Typical options:
    - first,last,birthday
    - last,first,birthday
    Birthday should parse with the same HW1 rules or ISO format.
    """
    try:
        with open(CONTACTS_FILE, newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            count = 0
            for row in reader:
                if not row:
                    continue

                # TODO: Adjust indexes to match the provided CSV layout
                # Example layout: first,last,birthday
                first = row[0].strip().lower()
                last = row[1].strip().lower()
                bday_raw = row[2].strip()

                bday = parse_date_hw1_rules(bday_raw)
                if bday is None:
                    continue

                insert_sorted(contacts, Contact(last, first, bday))
                count += 1

        print(f"Imported {count} contacts.")
    except FileNotFoundError:
        print(f"File not found: {CONTACTS_FILE}")
    except Exception as ex:
        print("Import failed.")
        print(type(ex), ex)


def export_contacts(contacts: list[Contact]) -> None:
    """
    Exports to the same filename as import: CONTACTS_FILE.
    TODO: write the same CSV layout used by import.
    """
    try:
        with open(CONTACTS_FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            for c in contacts:
                # TODO: Match import column order
                writer.writerow([c.first_name, c.last_name, c.birthday_iso()])
        print(f"Exported {len(contacts)} contacts.")
    except Exception as ex:
        print("Export failed.")
        print(type(ex), ex)


def display_contacts(contacts: list[Contact]) -> None:
    if len(contacts) == 0:
        print("No contacts to display.")
        return

    # Requirement format:
    # "Last Name, First Name   Birthdate   Age"
    # Title case names, date as yyyy-mm-dd, aligned columns
    header_name = "Last Name, First Name"
    header_bday = "Birthdate"
    header_age = "Age"
    print(f"{header_name:<28}{header_bday:<14}{header_age:>3}")

    for c in contacts:
        name = f"{c.display_last()}, {c.display_first()}"
        bday = c.birthday_iso()
        age = c.age_current_year()
        print(f"{name:<28}{bday:<14}{age:>3}")


def find_contact_index(contacts: list[Contact], first: str, last: str) -> int:
    first = first.strip().lower()
    last = last.strip().lower()
    for i, c in enumerate(contacts):
        if c.first_name == first and c.last_name == last:
            return i
    return -1


def delete_contact(contacts: list[Contact]) -> None:
    first = input("Enter first name to delete: ")
    last = input("Enter last name to delete: ")

    idx = find_contact_index(contacts, first, last)
    if idx < 0:
        print("Contact not found.")
        return

    c = contacts[idx]
    print("Found:")
    display_contacts([c])

    confirm = input("Delete this contact? (Y/N): ").strip().lower()
    if confirm == "y":
        contacts.pop(idx)
        print("Contact deleted.")
    else:
        print("Delete cancelled.")


def main():
    print_header()
    contacts: list[Contact] = []

    while True:
        choice = menu_choice()
        print()

        if choice == "1":
            c = input_contact()
            if c is not None:
                insert_sorted(contacts, c)
                print("Contact added.")
        elif choice == "2":
            import_contacts(contacts)
        elif choice == "3":
            display_contacts(contacts)
        elif choice == "4":
            export_contacts(contacts)
        elif choice == "5":
            delete_contact(contacts)
        elif choice == "6":
            print("HW2 Complete")
            break
        else:
            print("Invalid choice.")

        print()


if __name__ == "__main__":
    main()