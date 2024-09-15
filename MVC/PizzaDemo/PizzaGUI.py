import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter.messagebox import showinfo
from OrderController import OrderController

lincolnPizza = OrderController("Lincoln Pizza")

# root window
root = tk.Tk()
root.geometry('500x600')
root.resizable(False, False)
root.title('Lincoln Pizza House Order App')

def calcPrice():
    topList = []
    if memberStat.get() == 'Y':
        discountStat = True
    else:
        discountStat = False

    if cheese.get():
        topList.append('Cheese')
    if pep.get():
        topList.append('Pepperoni')
    if bacon.get():
        topList.append('Bacon')
    if seafood.get():
        topList.append('Seafood')
    if veggie.get():
        topList.append('Vegetables')

    theOrderTotal = lincolnPizza.addOrderList(pizzaSize.get(), drinkType.get(), topList, discountStat)
    subtotal.set(str("${0:.2f}".format(theOrderTotal[0])))
    gst.set(str("${0:.2f}".format(theOrderTotal[1])))
    total.set(str("${0:.2f}".format(theOrderTotal[2])))


def resetValues():
    memberStat.set(None)
    pizzaSize.set(None)
    drinkType.set(None)
    cheese.set(0)
    pep.set(0)
    bacon.set(0)
    seafood.set(0)
    veggie.set(0)
    subtotal.set("")
    gst.set("")
    total.set("")

def summary():
    totalOrder = lincolnPizza.orderTotal()
    numOrder = lincolnPizza.numOrder()
    msgSummary = "Number of Order: %2d \nTotal Order: $%.2f" %(numOrder, totalOrder)
    messagebox.showinfo(title='Summary', message= msgSummary)
    root.destroy()
    
#Create the Label
lblHeader = ttk.Label(root,text='Lincoln Pizza House', font=("Arial bold", 20))

lblHeader.pack(ipadx=10, ipady=10)


# label frame
frmMembership = ttk.LabelFrame(root, text='Membership')
frmMembership.pack(padx=5, pady=5)

memberStat = tk.StringVar()

# Member radio button
member_radio = ttk.Radiobutton(frmMembership,text='Member', value="Y", variable=memberStat)
member_radio.pack(ipadx=5, ipady=5, side='left')

nonMember_radio = ttk.Radiobutton(frmMembership,text='Non-Member', value="N", variable=memberStat)
nonMember_radio.pack(ipadx=5, ipady=5, side='left')

#label frame1
frmFrame1 = ttk.LabelFrame(root)
frmFrame1.pack()

#pizza size radio button
# label frame
frmPizzaSize = ttk.LabelFrame(frmFrame1, text='Pick Your Size')
frmPizzaSize.pack(ipadx=10, ipady = 10,  expand=True, side='left')

pizzaSize = tk.StringVar()

radLarge = ttk.Radiobutton(frmPizzaSize,text='Large', value="L", variable=pizzaSize)
radLarge.pack(padx=5,pady=2, anchor='w')

radMedium = ttk.Radiobutton(frmPizzaSize,text='Medium', value="M", variable=pizzaSize)
radMedium.pack(padx=5, pady=2,anchor='w')

radSmall = ttk.Radiobutton(frmPizzaSize,text='Small', value="S", variable=pizzaSize)
radSmall.pack(padx=5, pady=2,anchor = 'w')

#drink type radio button
# label frame
frmDrinkType = ttk.LabelFrame(frmFrame1, text='Pick Your Drink')
frmDrinkType.pack(ipadx=10, ipady=10, expand=True, side='left')

drinkType = tk.StringVar()

radFizzy = ttk.Radiobutton(frmDrinkType,text='Fizzy Drink', value="Fizzy", variable=drinkType)
radFizzy.pack(padx=5,pady=2, anchor='w')

radCoffee = ttk.Radiobutton(frmDrinkType,text='Coffee', value="Coffee", variable=drinkType)
radCoffee.pack(padx=5,pady=2, anchor='w')

radCapuccino = ttk.Radiobutton(frmDrinkType,text='Capuccino', value="Capuccino", variable=drinkType)
radCapuccino.pack(padx=5,pady=5, anchor = 'w')

radTea = ttk.Radiobutton(frmDrinkType,text='Tea', value="Tea", variable=drinkType)
radTea.pack(padx=5,pady=2, anchor = 'w')


#label frame1
frmFrame2 = ttk.LabelFrame(root)
frmFrame2.pack()

#checkbox for topping
# label frame
frmTopping = ttk.LabelFrame(frmFrame2, text='Pick Your Toppings')
frmTopping.pack(padx=10, pady = 10,  expand=True, fill='both', side='left')

cheese = tk.BooleanVar()
pep = tk.BooleanVar()
bacon = tk.BooleanVar()
seafood = tk.BooleanVar()
veggie = tk.BooleanVar()

chkCheese = ttk.Checkbutton(frmTopping, text='Extra Cheese', variable=cheese, onvalue=True, offvalue=False)
chkCheese.pack(padx=5,pady=2, anchor = 'w')

chkPepperoni = ttk.Checkbutton(frmTopping, text='Pepperoni', variable=pep, onvalue=True, offvalue=False)
chkPepperoni.pack(padx=5,pady=2, anchor = 'w')

chkBacon = ttk.Checkbutton(frmTopping, text='Bacon', variable=bacon, onvalue=True, offvalue=False)
chkBacon.pack(padx=5,pady=2, anchor = 'w')

chkSeafood = ttk.Checkbutton(frmTopping, text='Seafood', variable=seafood, onvalue=True, offvalue=False)
chkSeafood.pack(padx=5,pady=2, anchor = 'w')

chkVeggies = ttk.Checkbutton(frmTopping, text='Vegetables', variable=veggie, onvalue=True, offvalue=False)
chkVeggies.pack(padx=5,pady=2, anchor = 'w')

#Price frame
frmPrice = ttk.LabelFrame(frmFrame2, text='Price')
frmPrice.pack(padx=10, pady = 10,  expand=True, fill='both')

subtotal = tk.StringVar()
gst = tk.StringVar()
total = tk.StringVar()

lblSubTotal = tk.Label(frmPrice, text="Subtotal")
lblSubTotal.pack()

txtSubTotal = tk.Entry(frmPrice, textvariable=subtotal, state='disable')
txtSubTotal.pack()

lblGST = tk.Label(frmPrice, text="GST")
lblGST.pack()

txtGST = tk.Entry(frmPrice, textvariable=gst, state='disabled')
txtGST.pack()

lblTotal = tk.Label(frmPrice, text="Total")
lblTotal.pack()

txtTotal = tk.Entry(frmPrice, textvariable=total, state='disabled')
txtTotal.pack()

#button frame
frmButton = ttk.LabelFrame(root)
frmButton.pack(padx=5, pady=5, expand=True)

btnCalculate = ttk.Button(frmButton, text="Calculate", command = calcPrice )
btnCalculate.pack(padx=5,pady=2, side='left')

btnReset = ttk.Button(frmButton, text="Reset Form", command = resetValues )
btnReset.pack(padx=5,pady=2, side='left')

btnExit = ttk.Button(frmButton, text="Exit", command = summary)
btnExit.pack(padx=5,pady=2, side='left')

root.mainloop()
