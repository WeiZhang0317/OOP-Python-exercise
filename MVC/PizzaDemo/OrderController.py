from Order import Order

class OrderController:
    def __init__(self, outletName):
        self.outletName = outletName
        self.orderList = []

    def addOrderList(self, pType, dType, topList, mStat):
        anOrder = Order(pType, dType, topList, mStat)
        self.orderList.append(anOrder)
        return anOrder.calcPrice()
    
    def orderTotal(self):
        total = 0
        for order in self.orderList:
            sTotal = order.calcPrice()
            total += sTotal[2]
        return total

    def numOrder(self):
        return len(self.orderList)


