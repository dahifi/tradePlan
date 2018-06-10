class Position:

    def __init__(self, currency):
        self.currency = currency
        self.amount = 0
        self.wallets = []

    def add_wallet(self, wallet):
        self.wallets = wallet




