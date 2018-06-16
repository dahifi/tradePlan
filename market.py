from coinmarketcap import Market as CMC
import json
from currency import Currency


class Market:
    cmc = CMC()
    listings = cmc.listings()['data']

    class Currency:

        def __init__(self, symbol):
            self.symbol = symbol.upper()
            for listing in Market.listings:
                if listing['symbol'] == self.symbol:
                    self.listing = listing
                    self.token_id = listing['id']
                    self.name = listing['name']
                    self.get_ticker('btc')
                    #self.get_ticker('eth')
                    return
            else:
                raise Exception("Listing not found")


        def get_ticker(self, basecurrency=None):
            self.ticker = Market.cmc.ticker(self.token_id, convert=basecurrency)
            self.quote_btc = self.ticker['data']['quotes']['BTC']
            self.price_btc = self.quote_btc['price']
            self.quote_usd = self.ticker['data']['quotes']['USD']
            self.price_usd = self.quote_usd['price']
            return self.ticker



def lookup_currency(symbol, basecurrency=None):
        symbol = symbol.upper()
        for listing in Market.listings:
            if listing['symbol'] == symbol:
                token = Market.cmc.ticker(listing['id'], convert=basecurrency)
                return token
        else:
            raise NameError("Not valid token")




if __name__ == '__main__':

    holdings = {
        'btcp': 0.71323659,
        'xhv' : 302.6936943,
        'xmr' : 0.35750075,
        'rvn' : 18958.78413289,
        'zec' : 0.23915751, 
        'zcl' : 0.71374659,
        'xzc': 2.23439361
    }

    total_btc = 0
    total_usd = 0

    for coin, quantity in holdings.items():
        print(coin)
        bag = Market.Currency(coin)

        value_btc = bag.price_btc * quantity
        value_usd = bag.price_usd * quantity

        total_btc += value_btc
        total_usd += value_usd

    output = """
    Total BTC: {}
    Total USD: {}
    """.format(total_btc, total_usd)

    print(output)















