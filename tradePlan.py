

import datetime
import sys
import json
from decimal import *
import Exchange
from bittrex.bittrex import Bittrex
my_bittrex = Bittrex(None, None)

this = sys.modules[__name__]

MAX_LOSS_PERCENTAGE = 0.02  # Two percent
BASE_CURRENCY = "BTC"
CAPITAL_TOTAL = 0.4  # BTC

currencies = []
exchange = my_bittrex.get_currencies()['result']
for currency in exchange:
    currencies.append(currency['Currency'])


class TradePlan(object):
    """
    All the information about a planned, active, or closed trade
    Methods w/o underscore are public, underscores used for internal recalculations
    """

    def __init__(self, currency, capital=CAPITAL_TOTAL):
        """
        Intializes basic information to start plan
        """

        #common parameters
        self.CapitalToDeploy = capital if capital is not None else CAPITAL_TOTAL
        self.Created = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        self.BTCPrice = Exchange.quote('BTC')
        self.MarketCurrency = currency
        self.MarketName = BASE_CURRENCY + "-" + self.MarketCurrency
        if (not self.setCurrentPrice()): return #ticker not found

        self.EntryPrice = self.CurrentPrice #initialy planned, needs to lock for open positions
        self.ExitPricePlanned = self.EntryPrice * 1.3 # 30% gain
        self.PurchaseMax = CAPITAL_TOTAL / self.EntryPrice
        self.LossMax = CAPITAL_TOTAL * MAX_LOSS_PERCENTAGE
        self.StopLossMax = (CAPITAL_TOTAL - self.LossMax) / self.PurchaseMax

        self._setPurchaseAdjusted()
        self._setStopLossAdjusted()
        self.StopLossPlanned = self.StopLossMax

        self._setProceedsPlanned()
        self._setCapitalRisked


        #for open positions
        # self.CurrentChange = (self.CurrentPrice - self.EntryPrice) / self.EntryPrice
        #
        # #for closed positions
        # self.ExitPriceActual = self.ExitPricePlanned
        # self.ProceedsActual = self.PurchaseAdjusted * self.ExitPriceActual
        # self.Profit = (self.ProceedsActual - self.CapitalToDeploy) - 1
        #
        self.show()

    def show(self):
        output = """
        Market: {market}
        Current Price: {price}
        Entry Price: {entry}
        Quantity: {quantity}
        Stop: {stop}
        """.format(
            market=self.MarketName,
            price=ToSats(self.CurrentPrice),
            entry=ToSats(self.EntryPrice),
            quantity=self.PurchaseAdjusted,
            stop=ToSats(self.StopLossAdjusted),

        )

        print(output)
        # print(self.toJSON())
        """TODO: still no easy fix for json dump with satoshi price"""

    def setCapital(self, amount):
        self.CapitalToDeploy = amount
        self._setPurchaseAdjusted()
        self._setStopLossAdjusted()
        self.show()

    def setEntry(self, amount):
        self.EntryPrice = amount
        self._setPurchaseAdjusted()
        self._setCapitalRisked
        self.show()

    def setExit(self, amount):
        self.ExitPricePlanned = amount
        self._setProceedsPlanned()

    def _setPurchaseAdjusted(self):
        self.PurchaseAdjusted = self.CapitalToDeploy / self.EntryPrice
        self._setProceedsPlanned()

    def _setStopLossAdjusted(self):
        self.StopLossAdjusted = (self.CapitalToDeploy - self.LossMax) / self.PurchaseAdjusted

    def _setCapitalRisked(self):
        self.CapitalRisked = (self.EntryPrice - self.StopLossPlanned) * self.PurchaseAdjusted

    def _setProceedsPlanned(self):
        self.ProceedsPlanned = self.PurchaseAdjusted * self.ExitPricePlanned

    def toJSON(self):
        return json.dumps(self,default=lambda o:o.__dict__,
            sort_keys=True, indent=4)

    # try block may be unnecessary since addition of TradePlan.currencies check.
    def setCurrentPrice(self):
        try:
            self.CurrentPrice = my_bittrex.get_ticker(self.MarketName)['result']['Last']
            return True
        except TypeError:
            print("Market not valid. Try again")
            return False

    def execute(self):
        output = """
        Executing Trade Plan with {capital} BTC:
        {market} @ {entry} satoshis x {purchase} quantity
        Stop @ {stop}
        Exit @ {exit}
        """.format(
            capital=self.CapitalToDeploy,
            market=self.MarketName,
            entry=ToSats(self.EntryPrice),
            purchase=self.PurchaseAdjusted,
            stop=ToSats(self.StopLossAdjusted),
            exit=ToSats(self.ExitPricePlanned),
        )

        print(output)

    def isValid(token):
        if not (token in this.currencies):
            print("Currency not found.")
            return False
        else:
            return True


def ToSats(float):
    """
    Converts float in scientific notation to Satoshi value
    :param float: price of currency
    :return: same price in millionths of currency
    """

    return round(Decimal(float), 8)




if __name__ == '__main__':

    myTrade = TradePlan("PIVX", 0.1)
