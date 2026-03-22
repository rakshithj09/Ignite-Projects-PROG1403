import csv
from pathlib import Path
from contact import Contact
from bst import BinarySearchTree
from datetime import datetime


FILE_NAME = Path(__file__).resolve().parent / "Contacts.csv"


class DataManager:
    def __init__(self):
        self.tree = BinarySearchTree()

    def add_contact(self, contact):
        self.tree.add(contact)

    def import_from_csv(self, filepath = None):
        path = FILE_NAME if filepath is None else Path(filepath)
        count = 0
        try:
            with open(path, newline = "", encoding = "utf-8-sig") as f:
                reader = csv.reader(f)
                for row in reader:
                    if len(row) < 3:
                        continue
                    first, last, birthday = row[0:3]
                    phone = row[3] if len(row) > 3 else ""
                    bd = self._parse_date(birthday)
                    contact = Contact(last.strip(), first.strip(), bd, phone)
                    self.add_contact(contact)
                    count += 1
            if count:
                return True, f"Loaded {count} contacts."
            return False, "No contacts loaded."
        except Exception as ex:
            return False, f"Import failed: {ex}"

    def export_to_csv(self, filepath = None, contacts = None):
        path = FILE_NAME if filepath is None else Path(filepath)
        rows = contacts if contacts is not None else self.all_contacts()
        try:
            with open(path, "w", newline = "", encoding = "utf-8") as f:
                writer = csv.writer(f)
                for c in rows:
                    writer.writerow([c.first_name, c.last_name, c.get_birthdate_str(), c.phone])
            return True, f"Exported {len(rows)} contacts."
        except Exception as ex:
            return False, f"Export failed: {ex}"

    def all_contacts(self):
        return self.tree.traverse_in_order()

    def find(self, last, first):
        return self.tree.find(last, first)

    def delete(self, last, first):
        return self.tree.delete(last, first)

    def edit(self, last, first, new_contact):
        return self.tree.edit(last, first, new_contact)

    def search_by_field(self, field, value):
        value = value.strip().lower()
        matches = []
        for c in self.tree.traverse_in_order():
            if field == "last" and c.last_name == value:
                matches.append(c)
            elif field == "first" and c.first_name == value:
                matches.append(c)
            elif field == "birthdate" and c.get_birthdate_str() == value:
                matches.append(c)
            elif field == "phone" and c.phone.endswith(value):
                matches.append(c)
        return matches

    def _parse_date(self, text):
        txt = (text or "").strip()
        if not txt:
            return None
        for fmt in ("%m/%d/%Y", "%m/%d/%y", "%Y-%m-%d"):
            try:
                parsed = datetime.strptime(txt, fmt).date()
                return parsed
            except Exception:
                continue
        return None
