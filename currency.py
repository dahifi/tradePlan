


class Currency:



    def __init__(self, json):
        # name, symbol, cmc_id, cmc_slug
        self.name = json['name']
        self.symbol = json['symbol']
        self.id = json['id']
        self.slug = json['website_slug']

        self.price = 0
        self.exchanges = []
        self.wallets = []

    def __repr__(self):
        return "<Currency: %s Price: %s" % (self.name, self.price)