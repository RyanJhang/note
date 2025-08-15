# controllers/stock_price_set_controller.py
import flet as ft
from views.stock_price_set_view import stock_price_set_view


class StockPriceSetController:
    def __init__(self, stock_model):
        self.stock_model = stock_model

    def handle_stock_price_set(self, page: ft.Page, stock_symbol: str, new_price: float):
        stock_price_set_view(page, self.stock_model, stock_symbol, new_price)
