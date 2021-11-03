import requests, json
import alpaca_trade_api as tradeapi

#Setting all global keys and urls
paperkey = '<your paper key>'
papersecret = '<your secret key>'
paperurl = '<your url>'


realkey = '<your real key>'
realsecret ='<your secret key>'
realurl = '<your url>'

#switch for real when you want to trade with real money
APCA_API_KEY_ID= paperkey
APCA_API_SECRET_KEY=papersecret
APCA_API_BASE_URL=paperurl

ACCOUNT_URL="{}/v2/account".format(APCA_API_BASE_URL)
ORDERS_URL = "{}/v2/orders".format(APCA_API_BASE_URL)
HEADERS = {'APCA-API-KEY-ID':APCA_API_KEY_ID,'APCA-API-SECRET-KEY':APCA_API_SECRET_KEY}


api = tradeapi.REST(APCA_API_KEY_ID, APCA_API_SECRET_KEY, APCA_API_BASE_URL, api_version='v2')


account = api.get_account()
#print(account)

r = requests.get(ACCOUNT_URL, headers=HEADERS)


def get_profit_per_stock():
    activities = api.get_activities()
    buys = []
    sells = []
    pnl_list = []

    for each in activities:
        symbol = each.symbol

        # Create list of all the buys
        if each.symbol == symbol and each.side == 'buy':
            cash_spent = float(each.price) * float(each.qty)
            buys.append((each.symbol, cash_spent))
            print('cash_spent is:', cash_spent)

        # Create list of sells
        if each.symbol == symbol and each.side == 'sell':
            cash_taken = float(each.price) * float(each.qty)
            sells.append((each.symbol, cash_taken))

        # In case there are partial fills in the buys list this will merge them
        d = {x: 0 for x, _ in buys}
        for name, num in buys: d[name] += num
        merged_buys = list(map(tuple, d.items()))

        # In case there are partial fills in the sells list this will merge them
        e = {x: 0 for x, _ in sells}
        for name, num in sells: e[name] += num
        merged_sells = list(map(tuple, e.items()))

        # This is a list of tuples listing (symbol, total money spent on the buys, total money spent on the sells)
        transaction_list = [x + y[1:] for x in merged_sells for y in merged_buys if x[0] == y[0]]

        # This simply gives you the Profit/Loss for each symbol in the transaction list
        for each in transaction_list:
            symbol = each[0]
            pnl = round(float(each[1]) - float(each[2]), 2)
            pnl_list.append([symbol, pnl])

        return pnl_list
    
#WIP
def get_profit(write = False):
    activities = api.get_activities()
    buys = []
    sells = []
    pnl_list = []
    for each in activities:
        symbol = each.symbol
        print(symbol)
        if each.symbol == symbol and each.side == 'buy':
            cash_spent = float(each.price) * float(each.qty)
            buys.append((each.symbol, cash_spent))
            print('Bought', float(each.qty), symbol, 'at', float(each.price))
        if each.symbol == symbol and each.side == 'sell':
            cash_taken = float(each.price) * float(each.qty)
            sells.append((each.symbol, cash_taken))
            print('Sold', float(each.qty), symbol, 'at', float(each.price))
            
            

#get_profit()
            