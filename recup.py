from urllib import request
from usefull import formatted_price_and_time
import json


_list_url = "https://api.coinmarketcap.com/v1/ticker/"
_list_json = json.load(request.urlopen(_list_url))
name_list = {e["symbol"]: e["id"] for e in _list_json}


def get_id(currency_short_name: str) -> str:
    """
    return the long name for the coinmarketcap website
    """
    if currency_short_name in name_list.keys():
        return name_list[currency_short_name]
    else:
        raise AttributeError(
            f"The selected currency is not available : {currency_short_name} not found.\n"
            + "\n".join([f"\t{k}\t{v}" for k, v in name_list.items()])
        )


def get_data(curr: str) -> dict:
    """
    Get from the coinmarketcap' api some bitcoin's informations
    """
    bitcoin_api_url = f"https://api.coinmarketcap.com/v1/ticker/{get_id(curr)}/"
    response = request.urlopen(bitcoin_api_url)
    response_json = json.load(response)
    return response_json[0]


def price_usd(curr: str):
    return float(get_data(curr)["price_usd"])


if __name__ == "__main__":
    import time
    import datetime

    prec = None
    while True:
        time.sleep(1)
        cur: float = price_usd("BTC")
        if prec != cur:
            now: datetime = datetime.datetime.now()
            print(formatted_price_and_time(now, cur))
            prec = cur
