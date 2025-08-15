# models/stock_price_query_model.py
class StockModel:
    def __init__(self):
        self.stock_prices = {}

    def get_price(self, symbol):
        return self.stock_prices.get(symbol, "價格未知")

    def set_price(self, symbol, price):
        self.stock_prices[symbol] = price
