# main.py
import flet as ft
from controllers.stock_price_query_controller import StockPriceQueryController
from controllers.stock_price_set_controller import StockPriceSetController
from models.stock_price_query_model import StockModel as QueryStockModel
from models.stock_price_set_model import StockModel as SetStockModel


class RouteManager:
    def __init__(self, page: ft.Page, query_controller: StockPriceQueryController, set_controller: StockPriceSetController):
        self.page = page
        self.query_controller = query_controller
        self.set_controller = set_controller

    def add_routes(self):
        self.page.views.append(
            ft.TemplateRoute(
                route="/stock/price/query/{stock_symbol}",
                handler=self.stock_price_query_handler
            )
        )
        
        self.page.routes.append(
            ft.TemplateRoute(
                route="/stock/price/set/{stock_symbol}/{new_price}",
                handler=self.stock_price_set_handler
            )
        )

    def stock_price_query_handler(self, page: ft.Page, stock_symbol: str):
        self.query_controller.handle_stock_price_query(page, stock_symbol)

    def stock_price_set_handler(self, page: ft.Page, stock_symbol: str, new_price: float):
        self.set_controller.handle_stock_price_set(page, stock_symbol, new_price)

def main(page: ft.Page):
    query_stock_model = QueryStockModel()
    set_stock_model = SetStockModel()

    query_controller = StockPriceQueryController(query_stock_model)
    set_controller = StockPriceSetController(set_stock_model)

    route_manager = RouteManager(page, query_controller, set_controller)

    # 使用 RouteManager 來添加路由
    route_manager.add_routes()

    # 設定首頁路由
    page.add(ft.Text("歡迎來到股票價格查詢和設置系統"))

if __name__ == "__main__":
    ft.app(target=main)
