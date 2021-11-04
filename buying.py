import alpaca_trade_api as tradeapi
import requests, json
from config import *
from getdata import *
from datetime import datetime
from keys import *


ACCOUNT_URL="{}/v2/account".format(APCA_API_BASE_URL)
ORDERS_URL = "{}/v2/orders".format(APCA_API_BASE_URL)
HEADERS = {'APCA-API-KEY-ID':APCA_API_KEY_ID,'APCA-API-SECRET-KEY':APCA_API_SECRET_KEY}


api = tradeapi.REST(APCA_API_KEY_ID, APCA_API_SECRET_KEY, APCA_API_BASE_URL, api_version='v2')


account = api.get_account()
#print(account)

r = requests.get(ACCOUNT_URL, headers=HEADERS)



def get_account():
    r = requests.get(ACCOUNT_URL, headers=HEADERS)
    print(r.content)
    return json.loads(r.content)

def create_order(symbol, qty, side, typee, time_in_force, stop, loss):
    data = {
        "symbol" : symbol,
        "qty" : qty,
        "side": side,
        "type": typee,
        "time_in_force":time_in_force,
        "order_class": "bracket",
        "take_profit": {
            "limit_price": stop
        },
        "stop_loss": {
            "stop_price": loss
        }
    }
    r = requests.post(ORDERS_URL, json=data, headers=HEADERS)
    print(r.content)
    return json.loads(r.content)

def get_orders():
    r=requests.get(ORDERS_URL,headers=HEADERS)
    return json.loads(r.content)

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
    history = str(qty) + ' '+ symbol + ' bought at ' + str(datetime.now())
    write(history)
    return json.loads(r.content)

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
    history = str(qty) + ' '+ symbol + ' sold at ' + str(datetime.now())
    write(history)
    return json.loads(r.content)

#response = create_order("AAPL",100,'buy','market','gtc', 152, 140)
#print(response)
#sell = sell_order('AAPL',10,'market','gtc')


def live_sells(ticker, goal, qty, serious = False, refresh = 5):
    result = get_live_price(ticker, goal, refresh)
    if result == 'sell':
        print('WE SHOULD SELL NOW!')
        if serious:
            print('attempting to sell', qty, ticker)
            sell_order(ticker,qty,'market','gtc')

            
def write(text):
    historyfile = open('OrderHistory.txt', 'a')
    historyfile.write('\n')
    historyfile.write(text)
    historyfile.close()

#live_sells('AAPL',150.63, 50, serious = True, refresh = 2)




            
            
            
            
            