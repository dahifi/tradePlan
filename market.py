from coinmarketcap import Market as CMC
import json
from currency import Currency


class Market:
    cmc = CMC()
    listings = cmc.listings()['data']

    def currency(symbol, basecurrency=None):
        token = None
        convert = basecurrency
        for listing in Market.listings:
            if listing['symbol'] == symbol:
                #token = Currency(listing)
                #token.price = Market.cmc.ticker(token.id)
                token = Market.cmc.ticker(listing['id'], convert=convert)
        return token


if __name__ == '__main__':
    eth = Market.currency('SEN', 'BTC')
    print(json.dumps(eth, indent=2))

