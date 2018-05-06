

import datetime
from decimal import *
from bittrex.bittrex import Bittrex
my_bittrex = Bittrex(None, None)

MAX_LOSS_PERCENTAGE = 0.02  # Two percent
BASE_CURRENCY = "BTC"
CAPITAL_TOTAL = 0.4 #BTC

class TradePlan(object):
    """
    All the information about a planned, active, or closed trade
    """


    def __init__(self, currency, capital = CAPITAL_TOTAL ):
        """
        Intializes basic information to start plan
        """

        self.Created = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

        BTCPrice = 9655.00  ###<TODO> call BTC price from CMC or GDAX
        self.MarketCurrency = currency
        self.MarketName = BASE_CURRENCY + "-" + self.MarketCurrency
        self.CapitalToDeploy = capital if capital is not None else CAPITAL_TOTAL
        self.CurrentPrice = my_bittrex.get_ticker(self.MarketName)['result']['Last']
        self.EntryPrice = self.CurrentPrice
        self.PurchaseMax = CAPITAL_TOTAL / self.EntryPrice
        self.MaxLoss = CAPITAL_TOTAL * MAX_LOSS_PERCENTAGE
        self.StopLossMax = (CAPITAL_TOTAL - self.MaxLoss) / self.PurchaseMax

        self.PurchaseAdjusted = self.CapitalToDeploy / self.EntryPrice
        self.StopLossAdjusted = (self.CapitalToDeploy - self.MaxLoss) / self.PurchaseAdjusted
        self.StopLossPlanned = self.StopLossMax
        self.ExitPricePlanned = 0.0001389
        self.ProceedsPlanned = self.PurchaseAdjusted * self.ExitPricePlanned
        self.CapitalRisked = (self.EntryPrice - self.StopLossPlanned) * self.PurchaseAdjusted

        self.ExitPriceActual = self.ExitPricePlanned
        self.ProceedsActual = self.PurchaseAdjusted * self.ExitPriceActual
        self.Profit = (self.ProceedsActual - self.CapitalToDeploy) - 1

        self.CurrentChange = (self.CurrentPrice - self.EntryPrice) / self.EntryPrice
        self.show()

    def show(self):
        print ("Market: {} | Price: {} | Quantity: {} | Stop: {}".format(self.MarketName, ToSats(self.CurrentPrice), self.PurchaseAdjusted, ToSats(self.StopLossAdjusted)))

    def setCapital(self, amount):
        self.CapitalToDeploy = amount
        self.PurchaseAdjusted = self.CapitalToDeploy / self.EntryPrice
        self.StopLossAdjusted = (self.CapitalToDeploy - self.MaxLoss) / self.PurchaseAdjusted
        self.show()

    def setEntry(self, amount):
        self.EntryPrice = amount
        self.PurchaseAdjusted = self.CapitalToDeploy / self.EntryPrice
        self.CapitalRisked = (self.EntryPrice - self.StopLossPlanned) * self.PurchaseAdjusted
        self.show()


def ToSats(float):
    """
    Converts float in scientific notation to Satoshi value
    :param float: price of currency
    :return: same price in millionths of currency
    """

    return round(Decimal(float), 8)




if __name__ == '__main__':

    myTrade = TradePlan("PIVX", 0.1)



    """
    print("Capital: {} | Risk: {} | Max Loss: {}".format(__CapitalTotal__, CapitalDeployed, MaxLoss))
    print("Entry price: {} | Current price: {}".format(EntryPrice, CurrentPrice))
    print("Max purchase: {} | Adjusted purchase: {}".format(PurchaseMax, PurchaseAdjusted))
    print("Max stop: {} | Adjusted stop: {}".format(StopLossMax, StopLossAdjusted))
    print("Planned stop: {} | Capital Risk: {}".format(StopLossPlanned, CapitalRisked))
    """