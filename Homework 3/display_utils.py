from sales import Sales


def fmt_int(n, width):
    return f"{n:>{width},}"


def left(text, width):
    return f"{text:<{width}}"


def print_annual_table(title, rows):
    brand_w = 14
    model_w = 18
    val_w = 12

    print(title)
    print()
    print(left("Brand", brand_w) + left("Model", model_w) + f"{'Annual Sales':>{val_w}}")

    for row in rows:
        brand, model = row.get_name_fields()
        annual = row.get_annual_value()
        line = left(brand, brand_w) + left(model, model_w) + fmt_int(annual, val_w)
        print(line)

    print()


def print_monthly_table(title, rows):
    brand_w = 14
    model_w = 18
    mon_w = 8

    print(title)
    print()
    header = left("Brand", brand_w) + left("Model", model_w)
    for month in Sales.MONTHS:
        header += f"{month:>{mon_w}}"
    print(header)

    for row in rows:
        brand, model = row.get_name_fields()
        line = left(brand, brand_w) + left(model, model_w)
        for value in row.get_monthly_values():
            line += fmt_int(value, mon_w)
        print(line)

    print()
