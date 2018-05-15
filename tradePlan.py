

import datetime
import json
from decimal import *
from bittrex.bittrex import Bittrex
my_bittrex = Bittrex(None, None)

MAX_LOSS_PERCENTAGE = 0.02  # Two percent
BASE_CURRENCY = "BTC"
CAPITAL_TOTAL = 0.4 #BTC

class TradePlan(object):
    """
    All the information about a planned, active, or closed trade
    Methods w/o underscore are public, underscores used for internal recalculations

    """


    def __init__(self, currency, capital = CAPITAL_TOTAL ):
        """
        Intializes basic information to start plan
        """
        #common parameters

        self.CapitalToDeploy = capital if capital is not None else CAPITAL_TOTAL
        self.Created = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        #self.BTCPrice = 9655.00  ###<TODO> call BTC price from CMC or GDAX
        self.MarketCurrency = currency
        self.MarketName = BASE_CURRENCY + "-" + self.MarketCurrency

        self.CurrentPrice = my_bittrex.get_ticker(self.MarketName)['result']['Last']
        self.EntryPrice = self.CurrentPrice #initialy planned, needs to lock for open positions
        self.PurchaseMax = CAPITAL_TOTAL / self.EntryPrice
        self.LossMax = CAPITAL_TOTAL * MAX_LOSS_PERCENTAGE
        self.StopLossMax = (CAPITAL_TOTAL - self.LossMax) / self.PurchaseMax
        self._setPurchaseAdjusted()
        self._setStopLossAdjusted()
        self.StopLossPlanned = self.StopLossMax
        self.ExitPricePlanned = self.EntryPrice * 1.3 # 30% gain
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
        #print ("Market: {} | Price: {} | Quantity: {} | Stop: {}".format(self.MarketName, ToSats(self.CurrentPrice), self.PurchaseAdjusted, ToSats(self.StopLossAdjusted)))
        print(self.toJSON())

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
        self

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
        return json.dumps(self, default=lambda o: o.__dict__,
            sort_keys=True, indent=4)



def ToSats(float):
    """
    Converts float in scientific notation to Satoshi value
    :param float: price of currency
    :return: same price in millionths of currency
    """

    return round(Decimal(float), 8)




if __name__ == '__main__':

    myTrade = TradePlan("PIVX", 0.1)
