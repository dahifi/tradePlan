"""Module responsible for quoting prices, executing trades and monitoring open positions.
Right now only works with Bittrex but will be expanded to support Binance

"""
import json
from bittrex.bittrex import Bittrex
my_bittrex = Bittrex(None, None)

from coinmarketcap import Market

cmc = Market()
listings = cmc.listings()['data']


# count = listings['metadata']['num_cryptocurrencies']

def getCurrency(symbol):
    result = getexists(symbol)
    if result is not None:
        return cmc.ticker(result)['data']

def quote(symbol):
    result = getexists(symbol)
    if result is not None:
        return cmc.ticker(result)['data']['quotes']['USD']['price']

def getexists(symbol):
    for listing in listings:
        if listing['symbol'] == symbol:
            return listing['id']
        else:
            return None


if __name__ == '__main__':
    print(json.dumps(getCurrency('BTC'), indent=2))

