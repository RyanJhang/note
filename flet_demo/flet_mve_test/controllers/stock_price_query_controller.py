# controllers/stock_price_query_controller.py
import flet as ft
from views.stock_price_query_view import stock_price_query_view


class StockPriceQueryController:
    def __init__(self, stock_model):
        self.stock_model = stock_model

    def handle_stock_price_query(self, page: ft.Page, stock_symbol: str):
        stock_price_query_view(page, self.stock_model, stock_symbol)
