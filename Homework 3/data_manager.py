from brand import Brand
from model import Model
from sales import Sales


class DataManager:
    def __init__(self):
        self._brands = {}
        self._loaded = False

    def is_loaded(self):
        return self._loaded

    def clear(self):
        self._brands = {}
        self._loaded = False

    def get_brand(self, name):
        return self._brands.get(name)

    def brands_sorted(self):
        return sorted(self._brands.values(), key=lambda b: b.name.lower())

    def import_from_tsv(self, filepath):
        try:
            with open(filepath, "r", encoding="utf-8-sig", newline="") as f:
                lines = f.read().splitlines()
        except Exception as ex:
            return (False, f"File error: {ex}")

        header_index = self.find_header_index(lines)
        if header_index is None:
            return (False, "Header row not found. Expected Brand, Model, and 12 months.")

        header_cols = self.split_cols(lines[header_index])
        if not self.has_all_months(header_cols):
            return (False, "Month columns not found. Expected Jan..Dec in the header row.")

        self.clear()

        data_lines = lines[header_index + 1:]
        parsed_rows = 0

        for raw in data_lines:
            tokens = self.split_cols(raw)
            if len(tokens) < 14:
                continue

            month_tokens = tokens[-12:]
            name_tokens = tokens[:-12]
            if len(name_tokens) < 2:
                continue

            brand_name, model_name = self.split_brand_model(name_tokens)
            if not brand_name or not model_name:
                continue

            sales = Sales([self.safe_int(x) for x in month_tokens])
            brand = self._brands.setdefault(brand_name, Brand(brand_name))
            brand.add_model(Model(brand_name, model_name, sales))

            parsed_rows += 1

        if parsed_rows == 0:
            self.clear()
            return (False, "No data rows loaded.")

        self._loaded = True
        return (True, f"Loaded {parsed_rows} models across {len(self._brands)} brands.")

    def split_cols(self, line):
        return line.replace("\t", " ").split()

    def split_brand_model(self, name_tokens):
        # Handle known 2 word brands in this dataset
        two_word_brands = {("Alfa", "Romeo"), ("Land", "Rover")}

        if len(name_tokens) >= 3 and (name_tokens[0], name_tokens[1]) in two_word_brands:
            brand = f"{name_tokens[0]} {name_tokens[1]}"
            model = " ".join(name_tokens[2:]).strip()
            return brand, model

        # Default: first token is brand, rest is model
        brand = name_tokens[0].strip()
        model = " ".join(name_tokens[1:]).strip()
        return brand, model

    def safe_int(self, text):
        s = text.strip().replace(",", "")
        if s == "":
            return 0
        try:
            return int(float(s))
        except Exception:
            return 0

    def find_header_index(self, lines):
        for i, line in enumerate(lines):
            cols = [c.lower() for c in self.split_cols(line)]
            if len(cols) < 14:
                continue
            if cols[:2] == ["brand", "model"]:
                return i
            if {"brand", "model"}.issubset(cols[:3]):
                return i
        return None

    def has_all_months(self, header_cols):
        months = ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"]
        normalized = {c.strip().lower() for c in header_cols}
        return all(m in normalized for m in months)
