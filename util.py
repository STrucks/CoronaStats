

def prettify_number(number: int, delimiter=" ") -> str:
    """
    Transforms the inout number to a string and prettifies it with the given delimiter
    :param number:
    :return:
    """
    if type(number) == str:
        return number
    number_str = str(number)

    three_packs = []
    while len(number_str) > 3:
        three_packs.append(number_str[-3:])
        number_str = number_str[:-3]

    three_packs.append(number_str)
    pretty_number = delimiter.join(reversed(three_packs))
    return pretty_number


def prettify_datarow(row):
    """
    Cleans a data row that will be presented and makes it look pretty.
    :return:
    """

    for key in row.keys():
        if key in ["cases", "active_cases", "died", "cured"]:
            try:
                value = int(row[key])
                row[key] = prettify_number(value)
            except Exception:
                pass
        elif key in ["incidence"]:
            try:
                value = float(row[key])
                row[key] = str(round(value, 2))
            except Exception:
                pass
        else:
            pass
    return row