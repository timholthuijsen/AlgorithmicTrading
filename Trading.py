import alpaca_trade_api as tradeapi
import requests, json


#Here you need to define you ALPACA API trading keys or paper trading keys
paperkey = '<your key>'
papersecretkey = '<your secret key>'
paperurl = 'https://paper-api.alpaca.markets'


APCA_API_BASE_URL = paperurl
APCA_API_KEY_ID = paperkey
APCA_API_SECRET_KEY = papersecretkey



ACCOUNT_URL="{}/v2/account".format(APCA_API_BASE_URL)
ORDERS_URL = "{}/v2/orders".format(APCA_API_BASE_URL)
HEADERS = {'APCA-API-KEY-ID':APCA_API_KEY_ID,'APCA-API-SECRET-KEY':APCA_API_SECRET_KEY}

def buy_order(symbol, qty, typee, time_in_force):
    data = {
        "symbol" : symbol,
        "qty" : qty,
        "side": 'buy',
        "type": typee,
        "time_in_force":time_in_force,

    }
    r = requests.post(ORDERS_URL, json=data, headers=HEADERS)
    print(r.content)
    return json.loads(r.content)

#buy_order('V', 1, 'market', 'gtc')

def sell_order(symbol, qty, typee, time_in_force):
    data = {
        "symbol" : symbol,
        "qty" : qty,
        "side": 'sell',
        "type": typee,
        "time_in_force":time_in_force,

    }
    r = requests.post(ORDERS_URL, json=data, headers=HEADERS)
    print(r.content)
    return json.loads(r.content)

#Example of a buy order:
#buy_order('V', 1, 'market', 'gtc')