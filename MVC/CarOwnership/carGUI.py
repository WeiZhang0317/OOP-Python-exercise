import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo
from CarController import CarController

company = CarController()

def btnReadData():
    for i in range(1,6):
        lstbox_ppl.insert(tk.END, "PERSON" + str(i))
        company.newPerson("PERSON" + str(i))
    
    for j in range(1,6):
        lstbox_car.insert(tk.END, "CAR" + str(j))
        company.newCar("CAR" + str(j))

def btnChangeOwner():
    #get selected person
    selPersonIndex = lstbox_ppl.curselection()
    selectedPerson = lstbox_ppl.get(selPersonIndex)

    #get selected car
    selCarIndex = lstbox_car.curselection()
    selectedCar = lstbox_car.get(selCarIndex)

    #ask company to do the rest
    company.changeOwner(str(selectedPerson), str(selectedCar))

def btnWhoIsOwner():

    #get selected car
    selCarIndex = lstbox_car.curselection()
    selectedCar = lstbox_car.get(selCarIndex)

    #ask company to check
    theOwner = company.whoIsOwner(str(selectedCar))
    showinfo(title='Info', message= theOwner)
    

window = tk.Tk()
window.title("Car Ownership Application")
window.resizable(width=False, height=False)

#add the widgets
frm_formCreate= tk.Frame(relief=tk.FLAT, borderwidth=3)
# Pack the frame into the window
frm_formCreate.pack(padx=25, pady=5)

# button
button = ttk.Button(master=frm_formCreate,text="Create Objects",command=btnReadData)
button.pack(fill='x', padx=5, pady=5, side=tk.LEFT)

#add the widgets
frm_formDisp= tk.Frame(relief=tk.FLAT, borderwidth=3)
# Pack the frame into the window
frm_formDisp.pack(padx=25, pady=5)

lstbox_ppl = tk.Listbox(master=frm_formDisp, exportselection=0, selectmode=tk.BROWSE)
lstbox_ppl.pack(fill='x', padx=20, pady=5,side=tk.LEFT)

lstbox_car = tk.Listbox(master=frm_formDisp, exportselection=0, selectmode=tk.BROWSE)
lstbox_car.pack(fill='x', padx=20, pady=5,side=tk.LEFT)

frm_formButton = tk.Frame(relief=tk.FLAT, borderwidth=3)
# Pack the frame into the window
frm_formButton.pack()

# button
button1 = ttk.Button(master=frm_formButton,text="Change Owner",command=btnChangeOwner)
button1.pack(fill='x', padx=5, pady=5, side=tk.LEFT)

button2 = ttk.Button(master=frm_formButton,text="Who is the Owner",command=btnWhoIsOwner)
button2.pack(fill='x', padx=5, pady=5, side=tk.LEFT)

window.mainloop()
