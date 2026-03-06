from sales import Sales
from model import Displayable


def fmt_int(n, width):
    return f"{n:>{width},}"


def left(text, width):
    return f"{text:<{width}}"


def print_annual_table(title, rows):
    brand_w = 14
    model_w = 18
    val_w = 12

    header = left("Brand", brand_w) + left("Model", model_w) + f"{'Annual Sales':>{val_w}}"
    lines = (
        _row_prefix(r, brand_w, model_w) + fmt_int(r.get_annual_value(), val_w)
        for r in rows
    )
    print_table(title, header, lines)


def print_monthly_table(title, rows):
    brand_w = 14
    model_w = 18
    mon_w = 8

    header = left("Brand", brand_w) + left("Model", model_w) + "".join(f"{m:>{mon_w}}" for m in Sales.MONTHS)
    lines = (
        _row_prefix(r, brand_w, model_w) + "".join(fmt_int(v, mon_w) for v in r.get_monthly_values())
        for r in rows
    )
    print_table(title, header, lines)


def _row_prefix(row, brand_w, model_w):
    brand, model = row.get_name_fields()
    return left(brand, brand_w) + left(model, model_w)


def print_table(title, header, lines):
    print(title)
    print()
    print(header)
    for line in lines:
        print(line)
    print()
