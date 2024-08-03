#create Order class
# need membership, pizza size, drink and topping
class Order:
    '''This class is to process pizza orders
    Members get 10% discount'''
    def __init__(self, pSize, pDrink, pTopping, pMember):
        '''Initialise the attributes of the order'''
        self.pizzaSize = pSize
        self.pizzaDrink = pDrink
        self.pizzaTopping = pTopping
        self.pizzaMember = pMember

    def getPizzaPrice(self):
        '''Calculates the cost of the pizza based on the size selected
        L is $15.00,  M is $12.00 and S is 10.00'''
        if self.pizzaSize == 'L':
            return 15.00
        elif self.pizzaSize == 'M':
            return 12.00
        else:
            return 10.00

    def getDrinkPrice(self):
        '''Calculates the drink price based on the drink selected
        Fizzy $4.00, Regular Coffee $5.00, Tea $3.00 and Cappuccino $6.00'''
        if self.pizzaDrink == "Fizzy":
            return 4.00
        elif self.pizzaDrink == "Regular Coffee":
            return 5.00
        elif self.pizzaDrink == "Tea":
            return 3.00
        else:
            return 6.00

    def getToppingPrice(self):
        '''Calculates the topping price, each additional topping is $1.00'''
        return len(self.pizzaTopping) * 1.00

    def calcTotal(self):
        '''Calculates the total, members gets 10% discount, GST is 15%'''
        grossTotal = self.getPizzaPrice() + self.getDrinkPrice() + self.getToppingPrice()
        if self.pizzaMember:
            grossTotal = grossTotal * 0.9
        gst = grossTotal * 0.15
        netPrice = grossTotal + gst
        return netPrice
    
    def orderDetail(self):
        return f"Pizza Size: {self.pizzaSize} Drink: {self.pizzaDrink} Topping: {self.pizzaTopping} Price: ${self.calcTotal()}"

#create a list
orderList = []

#create order
anOrder = Order("L", "Fizzy", ["Extra Cheese", "Bacon", "Pepperoni"], True)
#print(anOrder.orderDetail())
orderList.append(anOrder)

anotherOrder = Order("L", "Cappuccino", ["Extra Cheese", "Bacon"], False)
#print(anotherOrder.orderDetail())
orderList.append(anotherOrder)

for orderItem in orderList:
    print(orderItem.orderDetail())