"""Module responsible for quoting prices, executing trades and monitoring open positions.
Right now only works with Bittrex but will be expanded to support Binance

"""

from bittrex.bittrex import Bittrex

my_bittrex = Bittrex(None, None)

from coinmarketcap import Market

cmc = Market()
listings = cmc.listings()['data']


# count = listings['metadata']['num_cryptocurrencies']

def quote(symbol):
    if getexists(symbol):
        id = listings['id']
        return cmc.ticker(id)['data']['quotes']['USD']['price']


def getexists(symbol):
    for listing in listings:
        if listing['symbol'] == symbol:
            return True
        else:
            return False


if __name__ == '__main__':
    print(quote('BTC'))
