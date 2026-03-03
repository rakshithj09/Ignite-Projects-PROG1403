from __future__ import annotations
from typing import Iterable

from sales import Sales
from model import Displayable


def fmt_int(n: int, width: int) -> str:
    return f"{n:>{width},}"


def left(text: str, width: int) -> str:
    return f"{text:<{width}}"


def print_annual_table(title: str, rows: list[Displayable]) -> None:
    print(title)
    print()

    brand_w = 14
    model_w = 18
    val_w = 12

    print(left("Brand", brand_w) + left("Model", model_w) + f"{'Annual Sales':>{val_w}}")

    for r in rows:
        b, m = r.get_name_fields()
        print(left(b, brand_w) + left(m, model_w) + fmt_int(r.get_annual_value(), val_w))

    print()


def print_monthly_table(title: str, rows: list[Displayable]) -> None:
    print(title)
    print()

    brand_w = 14
    model_w = 18
    mon_w = 8

    header = left("Brand", brand_w) + left("Model", model_w)
    for m in Sales.MONTHS:
        header += f"{m:>{mon_w}}"
    print(header)

    for r in rows:
        b, m = r.get_name_fields()
        line = left(b, brand_w) + left(m, model_w)
        for v in r.get_monthly_values():
            line += fmt_int(v, mon_w)
        print(line)

    print()