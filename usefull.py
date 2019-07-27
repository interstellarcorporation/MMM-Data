"""
Usefull thinks...

@date: 04/05/2019
@author: Quentin Lieumont
"""
import datetime
import json


# Readable outputs


def formatted_price(p) -> str:
    return "{} USD/BTC".format(p)


def formatted_time(t: datetime) -> str:
    return "{}h {}m {}s".format(
        str(t.hour).zfill(2), str(t.minute).zfill(2), str(t.second).zfill(2)
    )


def formatted_price_and_time(t, p) -> str:
    return "{}: {}".format(formatted_time(t), formatted_price(p))


# JSON parser


def get_json(link: str):
    return json.load(open(link, "r"))


def write_json(link: str, data) -> None:
    _json = json.dumps(data, sort_keys=True, indent=4, separators=(",", ": "))
    with open(link, "w") as f:
        for l in _json.split("\n"):
            f.write(l)


# Date file name management


def merge_date(date: datetime.date) -> str:
    """
    the date format is : ddmmyyyy
    for the file name
    :return ret: (str) the date formated like below
    """
    ret = str(date.day).zfill(2)
    ret += str(date.month).zfill(2)
    ret += str(date.year).zfill(4)
    return ret


def is_date(_file_name: str) -> datetime.date or None:
    """
    the date format is : ddmmyyyy
    :return : date if date found else None
    """
    # removing '.json'
    _file_name = _file_name[:-5]
    if len(_file_name) != 8:
        return None
    else:
        for c in _file_name:
            if c not in "0123456789":
                return None

        # All tests passed :)
        # building the date
        d = int(_file_name[0:2])
        m = int(_file_name[2:4])
        y = int(_file_name[4:8])
        return datetime.date(y, m, d)


def file_name(currency: str, date: datetime.date) -> str:
    return f"data/{currency}/{merge_date(date)}.json"


# get_price : WIP
"""
def get_price(
    date: datetime, flexibility: datetime.timedelta = datetime.timedelta(0)
) -> float or None:
    try:
        data = get_json(file_name(date))
    except FileNotFoundError:
        return None
    else:
        searcher = {"hour": date.hour, "minute": date.minute, "second": date.second}
        time_table = [d["time"] for d in data]
        if searcher in time_table:
            return data[time_table.index(searcher)]["price"]
        else:  # Search the closest neighbour
            closest = min(
                time_table,
                key=lambda t: abs(
                    (
                        datetime.datetime(
                            date.year,
                            date.month,
                            date.day,
                            t["hour"],
                            t["minute"],
                            t["second"],
                        )
                        - date
                    ).total_seconds()
                ),
            )
            if (
                abs(
                    (
                        date
                        - datetime.datetime(
                            date.year,
                            date.month,
                            date.day,
                            closest["hour"],
                            closest["minute"],
                            closest["second"],
                        )
                    ).total_seconds()
                )
                <= flexibility.total_seconds()
            ):
                return data[time_table.index(closest)]["price"]
            else:
                return None
"""
