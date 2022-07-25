from abc import ABC


class Logistics(ABC):

    # 初始化透過factory method創建product
    def __init__(self):
        self.product = self.factory_method()

	# 抽象的product創建方法
    def factory_method(self):
        pass

    # 卡車和船共通的送貨邏輯
    def run_delivery(self):
        print("Running some complex operations")
        self.product.deliver()

# 陸路運輸公司


class RoadLogistics(Logistics):

    # 重寫工廠方法
    def factory_method(self):
        return Truck()

# 海路運輸公司


class SeaLogistics(Logistics):

    # 重寫工廠方法
    def factory_method(self):
        return Ship()

# 廣義的運輸工具


class Transport(ABC):

	# 會運輸
	def deliver(self):
    	pass

# 貨車


class Truck(Transport):

    # 會走陸路運輸
    def deliver(self):
    	print("truck delivering stuff")

# 船


class Ship(Transport):

    # 會走海路運輸
    def deliver(self):
        print("ship delivering stuff")


if __name__ == "__main__":
	# 假設陸路運輸公司那邊要製造貨車來送貨
    logistics = RoadLogistics()
    logistics.run_delivery()
