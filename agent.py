from tradePlan import TradePlan as TP
import sys, json, pickle

###todo: read storage and list markets for all open positions ###

this = sys.modules[__name__]

activeCurrency = None
plans = {}


def market(currency):
    if currency not in plans:

        plan = TP(currency)
        plans[currency] = plan
    this.activeCurrency = plans[currency]


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


if __name__ == '__main__':
    ADA = market("ADA")
