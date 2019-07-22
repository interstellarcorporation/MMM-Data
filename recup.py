from urllib import request
from usefull import formatted_price_and_time
import json


def get() -> dict:
    """
    Get from the coinmarketcap' api some bitcoin's informations
    
    :return dict:
    """
    bitcoin_api_url = "https://api.coinmarketcap.com/v1/ticker/bitcoin/"
    response = request.urlopen(bitcoin_api_url)
    response_json = json.load(response)
    return response_json[0]


def price_btc_usd():
    return float(get()["price_usd"])


if __name__ == "__main__":
    import time
    import datetime

    prec = None
    while True:
        time.sleep(1)
        cur: float = price_btc_usd()
        if prec != cur:
            now: datetime = datetime.datetime.now()
            print(formatted_price_and_time(now, cur))
            prec = cur
