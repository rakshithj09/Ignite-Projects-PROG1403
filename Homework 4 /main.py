"""
 Course: PROG 1403 – Programming Logic 2
 Semester: Spring 2026
 Project: HW2 – Contact List
 Author: Rakshith Jayakarthikeyan, Abdullah Tabrez, Charlie Crandall
"""

import sys
from datetime import datetime
from data_manager import DataManager
def print_contacts(title, contacts):
	print(title)
	print()
	print(f"{'Last Name, First Name':<28} {'Birthdate':<12} {'Age':>3} {'Phone':<20}")
	for c in contacts:
		age = c.get_age()
		age_str = f"{age:>3}" if isinstance(age, int) else f"{age:>3}"
		print(f"{c.get_display_name():<28} {c.get_birthdate_str():<12} {age_str:>3} {c.phone_str():<20}")
	print()
from contact import Contact


def parse_date(text):
	text = (text or "").strip()
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
	return None


def print_menu():
	print("1. Enter a new Contact from the console")
	print("2. Import Contacts from a file")
	print("3. Display all Contacts on the console")
	print("4. Export all Contacts to a file")
	print("5. Delete a single Contact")
	print("6. Edit a single Contact")
	print("7. Display a selected subset of Contacts on the console")
	print("8. Export a selected subset of Contacts to a file")
	print("9. Exit")


def read_nonempty(prompt):
	while True:
		s = input(prompt).strip()
		if s:
			return s
		print("Please enter a value.")


def enter_contact(dm):
	first = read_nonempty("Enter first name: ")
	last = read_nonempty("Enter last name: ")
	bd = None
	while bd is None:
		bd = parse_date(input("Enter birthdate (m/d/y or yyyy-mm-dd): "))
		if bd is None:
			print("Invalid date. Try again or enter blank for none.")
	phone = input("Enter phone (digits and + allowed): ").strip()
	c = Contact(last, first, bd, phone)
	dm.add_contact(c)
	print("Contact added.")


def import_contacts(dm):
	ok, msg = dm.import_from_csv()
	print(msg)


def display_all(dm):
	contacts = dm.all_contacts()
	if not contacts:
		print("No contacts.")
		return
	print_contacts("All Contacts", contacts)


def export_all(dm):
	ok, msg = dm.export_to_csv()
	print(msg)


def delete_contact(dm):
	first = input("Enter first name to delete: ").strip()
	last = input("Enter last name to delete: ").strip()
	if dm.delete(last, first):
		print("Contact deleted.")
	else:
		print("Contact not found.")


def edit_contact(dm):
	first = input("Enter first name to edit: ").strip()
	last = input("Enter last name to edit: ").strip()
	cur = dm.find(last, first)
	if not cur:
		print("Contact not found.")
		return
	print("Leave a field blank to keep current value.")
	new_first = input(f"First name [{cur.first_name.title()}]: ").strip() or cur.first_name
	new_last = input(f"Last name [{cur.last_name.title()}]: ").strip() or cur.last_name
	bd_input = input(f"Birthdate [{cur.get_birthdate_str()}]: ").strip()
	bd = parse_date(bd_input) if bd_input else cur.birthday
	phone = input(f"Phone [{cur.phone_str()}]: ").strip() or cur.phone.digits
	new_contact = Contact(new_last, new_first, bd, phone)
	if dm.edit(last, first, new_contact):
		print("Contact updated.")
	else:
		print("Failed to update contact.")


def display_subset(dm):
	print("Search by field: last, first, birthdate, phone")
	field = input("Field: ").strip().lower()
	if field not in ("last", "first", "birthdate", "phone"):
		print("Invalid field.")
		return
	value = input("Value to match: ").strip()
	matches = dm.search_by_field(field, value)
	if not matches:
		print("No matches.")
		return
	print_contacts(f"Matches for {field} = {value}", matches)


def export_subset(dm):
	print("Export subset - choose field to match: last, first, birthdate, phone")
	field = input("Field: ").strip().lower()
	if field not in ("last", "first", "birthdate", "phone"):
		print("Invalid field.")
		return
	value = input("Value to match: ").strip()
	matches = dm.search_by_field(field, value)
	ok, msg = dm.export_to_csv(contacts = matches)
	print(msg)


def main():
	print("HW4 – Contact List, Version 2")
	print("Solution by CodePuppies")
	print()

	dm = DataManager()

	actions = {
		"1": enter_contact,
		"2": import_contacts,
		"3": display_all,
		"4": export_all,
		"5": delete_contact,
		"6": edit_contact,
		"7": display_subset,
		"8": export_subset,
	}

	while True:
		print_menu()
		choice = input("Enter choice: ").strip()
		print()
		if choice == "9":
			print("HW4 Complete")
			break
		action = actions.get(choice)
		if action:
			action(dm)
		else:
			print("Invalid choice.")
		print()


if __name__ == "__main__":
	main()

