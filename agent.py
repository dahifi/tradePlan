from tradePlan import TradePlan as TP
import sys, json

#read storage and list markets for all open positions

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




