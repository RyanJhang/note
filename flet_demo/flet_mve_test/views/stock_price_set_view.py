# views/stock_price_set_view.py
import flet as ft


def stock_price_set_view(page: ft.Page, stock_model, stock_symbol: str, new_price: float):
    stock_model.set_price(stock_symbol, new_price)
    page.add(ft.Text(f"已將股票 {stock_symbol} 的價格設置為 {new_price}"))
