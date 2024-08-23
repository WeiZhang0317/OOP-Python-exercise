from OrderController import OrderController

lincolnPizza = OrderController("Lincoln Pizza")

print ("Welcome to Lincoln Pizza")
pizzaSize = input("What is the size of your pizza (L)arge, (M)edium, (S)mall: ")
drinkType = input("What is your drink? Fizzy, Tea, Coffee or Cappucino ")
toppingReq = []
toppingList = ["Cheese", "Pepperoni", "Bacon", "Seafood", "Vegetarian"]
for extraTop in toppingList:
    response = input("Do you want {}? ".format(extraTop))
    if response == "Y":
        toppingReq.append(extraTop)
memberStat = input("Are you a member? Y/N ")

amount = lincolnPizza.addOrderList(pizzaSize, drinkType,toppingReq, memberStat)
print(amount[2])
print(lincolnPizza.orderTotal())L