class Order:
    def __init__(self, pizza, drink, toppingList, discount):
        self.pizzaSize = pizza
        self.drinkType = drink
        self.toppingList = toppingList
        self.discountStatus = discount

    def getPizzaPrice(self):
        if self.pizzaSize == "L":
            return 10.00
        elif self.pizzaSize == "M":
            return 8.00
        else:
            return 5.00

    def getDrinkPrice(self):
        if self.drinkType == "Fizzy":
            return 4.00
        elif self.drinkType =="Tea" or self.drinkType == "Coffee":
            return 5.00
        else:
            return 5.50

    def getToppingPrice(self):
        return len(self.toppingList) * 1.00

    def calcPrice(self):
        grossPrice = self.getPizzaPrice() + self.getDrinkPrice() + self.getToppingPrice()
        if self.discountStatus:
            grossPrice = grossPrice * 0.9
        gst = grossPrice * 0.15
        netPrice = grossPrice + gst
        return grossPrice, gst, netPrice
