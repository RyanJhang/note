# views/stock_price_query_view.py
import flet as ft


def stock_price_query_view(page: ft.Page, stock_model, stock_symbol: str):
    price = stock_model.get_price(stock_symbol)
    page.add(ft.Text(f"股票 {stock_symbol} 的價格是 {price}"))
