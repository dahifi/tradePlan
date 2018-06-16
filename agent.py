from tradePlan import TradePlan as TP
from position import Position
from currency import Currency
from market import Market
import sys
# import json
import pickle



"""TODO: read storage and list markets for all open positions"""

this = sys.modules[__name__]


activeToken = None
tokens = {}
activeCurrency = None
plans = {}


"""TODO: Make class and load on __init__"""


def token(symbol):
    if symbol not in tokens:
        new_coin = Market.currency(symbol)
        print (new_coin)
        tokens[symbol] = new_coin

    else:
        print("not found")
        return
    this.activeToken = new_coin
    return new_coin



def market(currency):
    currency = currency.upper()
    if currency not in plans:

        if TP.isValid(currency):
            plan = TP(currency)
            plans[currency] = plan
        else:
            return


    this.activeCurrency = plans[currency]



def show():
    this.activeCurrency.show()


def capital(amount):
    this.activeCurrency.setCapital(amount)


def entry(price):
    this.activeCurrency.setEntry(price)


def exit(price):
    this.activeCurrency.setExit(price)


def save():
    pickle.dump(plans, open("plans.p", "wb"))
    print("Plans saved")


def load():
    this.plans = pickle.load(open("plans.p", "rb"))

    """TODO: load will overwrite currently loaded plans. Make sure load only happens on program start"""


def execute():
    this.activeCurrency.execute()


this.load()

if __name__ == '__main__':
    pass