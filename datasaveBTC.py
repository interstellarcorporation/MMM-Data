"""
A simple scrypt to fill our database

@author: Quentin Lieumont
@date : 18/04/2019
"""
from datetime import datetime
from recup import price_btc_usd
import json
import shutil
from usefull import file_name


_dirty_global: bool = False  # <- if the file isn't created yet


def need_write(link, price: float = price_btc_usd()) -> bool:
    """
    As the price changed ?
    :param link: link to the file, create a file if it exit
    :param price: the current price to test
    :return: bool
    """
    global _dirty_global
    txt: str = ""
    try:
        with open(link, "r") as f:
            txt += f.readline()
            txt += f.readline()
            txt += "]"
    except FileNotFoundError:
        _dirty_global = True
        txt += "[]"
        with open(link, "w") as f:
            f.write("[\n]")
    finally:
        data = json.loads(txt)
        del txt
    if len(data) is 0:
        return True
    elif price == data[0]["price"]:
        return False
    else:
        return True


def write_price(link, price: float = price_btc_usd()) -> None:
    """
    Create new time/price dict and add it to the json
    :param link: link to the file
    :param price: the current price to write
    :return: None
    """
    global _dirty_global
    time = datetime.now().time()
    formated_time = (
        "{"
        + '"hour": {h}, "minute": {m}, "second": {s}'.format(
            h=time.hour, m=time.minute, s=time.second
        )
        + "}"
    )
    with open(link) as f_old, open("tmp", "w") as f_new:
        for i, line in enumerate(f_old):
            if i == 1:
                f_new.write(
                    "{"
                    + '"time": {t}, "price": {p}'.format(t=formated_time, p=price)
                    + "}"
                )
                if _dirty_global:
                    f_new.write("\n")
                else:
                    f_new.write(",\n")
            f_new.write(line)
    shutil.move("tmp", link)


if __name__ == "__main__":
    while True:
        datafile = file_name(datetime.now().date())
        current_price = price_btc_usd()
        if need_write(datafile, current_price):
            write_price(datafile, current_price)
