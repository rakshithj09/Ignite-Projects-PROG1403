from __future__ import annotations

from brand import Brand
from model import Model
from sales import Sales


class DataManager:
    def __init__(self):
        self._brands: dict[str, Brand] = {}
        self._loaded = False

    def is_loaded(self) -> bool:
        return self._loaded

    def clear(self) -> None:
        self._brands = {}
        self._loaded = False

    def brand_names_sorted(self) -> list[str]:
        return sorted(self._brands.keys(), key=lambda s: s.lower())

    def get_brand(self, name: str) -> Brand | None:
        return self._brands.get(name)

    def brands_sorted(self) -> list[Brand]:
        return [self._brands[n] for n in self.brand_names_sorted()]

    def import_from_tsv(self, filepath: str) -> tuple[bool, str]:
        try:
            with open(filepath, "r", encoding="utf-8-sig", newline="") as f:
                lines = f.read().splitlines()
        except Exception as ex:
            return (False, f"File error: {ex}")

        header_index = self._find_header_index(lines)
        if header_index is None:
            return (False, "Header row not found. Expected Brand, Model, and 12 months.")

        header_cols = self._split_cols(lines[header_index])
        month_indexes = self._map_month_columns(header_cols)
        if month_indexes is None:
            return (False, "Month columns not found. Expected Jan..Dec in the header row.")

        self.clear()

        data_lines = lines[header_index + 1:]
        parsed_rows = 0

        for raw in data_lines:
            if not raw.strip():
                continue

            tokens = self._split_cols(raw)

            # Need: name tokens + 12 monthly values
            if len(tokens) < 14:
                continue

            month_tokens = tokens[-12:]
            name_tokens = tokens[:-12]
            if len(name_tokens) < 2:
                continue

            brand_name, model_name = self._split_brand_model(name_tokens)
            if not brand_name or not model_name:
                continue

            monthly_values = [self._safe_int(x) for x in month_tokens]

            sales = Sales(monthly_values)
            model = Model(brand_name, model_name, sales)

            brand = self._brands.get(brand_name)
            if brand is None:
                brand = Brand(brand_name)
                self._brands[brand_name] = brand
            brand.add_model(model)

            parsed_rows += 1

        if parsed_rows == 0:
            self.clear()
            return (False, "No data rows loaded.")

        self._loaded = True
        return (True, f"Loaded {parsed_rows} models across {len(self._brands)} brands.")

    def _split_cols(self, line: str) -> list[str]:
        # Supports tabs or spaces, collapses repeats
        line = line.strip().replace("\t", " ")
        return line.split()

    def _split_brand_model(self, name_tokens: list[str]) -> tuple[str, str]:
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

    def _safe_int(self, text: str) -> int:
        s = text.strip().replace(",", "")
        if s == "":
            return 0
        try:
            return int(float(s))
        except Exception:
            return 0

    def _find_header_index(self, lines: list[str]) -> int | None:
        for i, line in enumerate(lines):
            cols = [c.strip() for c in self._split_cols(line)]
            if len(cols) < 14:
                continue
            if cols[0].lower() == "brand" and cols[1].lower() == "model":
                return i
            first_three = [c.lower() for c in cols[:3]]
            if "brand" in first_three and "model" in first_three:
                return i
        return None

    def _map_month_columns(self, header_cols: list[str]) -> list[int] | None:
        lookup = {c.strip().lower(): idx for idx, c in enumerate(header_cols)}
        months = ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"]
        indexes: list[int] = []
        for m in months:
            if m not in lookup:
                return None
            indexes.append(lookup[m])
        return indexes