import tkinter as tk
from tkinter import ttk
from BankAccount import BankAccount
from tkinter.messagebox import showinfo

anAcct = BankAccount(100.00, 10.00)

window = tk.Tk()
window.title("OO Bank Application")
window.resizable(width=False, height=False)

#add the widgets
frm_formRadio = tk.Frame(relief=tk.FLAT, borderwidth=3)
# Pack the frame into the window
frm_formRadio.pack(padx=25, pady=5, side=tk.LEFT)

frm_transAmt = tk.Frame(relief=tk.FLAT, borderwidth=3)
frm_transAmt.pack()

# Create a new frame `frm_formLeft`
frm_formLeft = tk.Frame(relief=tk.FLAT, borderwidth=3)
# Pack the frame into the window
frm_formLeft.pack()

frm_formButton = tk.Frame(relief=tk.FLAT, borderwidth=3)
# Pack the frame into the window
frm_formButton.pack()

def show_selected_size():

    if selected_size.get() != "D" and selected_size.get() != "W":
        showinfo(
        title='Result',
        message="Option Not Selected"
        )
    else:
        amount = float(ent_trans_amt.get())
        if (selected_size.get()=="W"):
            status = anAcct.withdraw(amount)
            if status == 1:
                showinfo(title='Info', message="Withdraw Successful")
            else:
                showinfo(title='Info', message="Withdraw Failed, Fee Applied")
            msgString = "Withdraw " + str(amount) + " Balance: " + str(anAcct.balance)
        else:
            anAcct.deposit (amount)
            showinfo(title='Info', message="Deposit Successful")
            msgString = "Deposit " + str(amount) + " Balance: " + str(anAcct.balance)
        
        txtbox_trans.insert(tk.END, msgString)
        txtbox_trans.insert(tk.END, "\n")

selected_size = tk.StringVar()
sizes = (('Deposit', 'D'),
        ('Withdraw', 'W'))

# label
label = ttk.Label(master= frm_formRadio, text="Transaction Type")
label.pack(fill='x', padx=0, pady=0 )

# radio buttons
for size in sizes:
    r = ttk.Radiobutton(
        master=frm_formRadio,
        text=size[0],
        value=size[1],
        variable=selected_size
    )
    r.pack(fill='x', padx=5, pady=5)

# label
label_tlist= ttk.Label(master=frm_formLeft, text="Transaction List")
label_tlist.pack(fill='x', padx=20, pady=5)

txtbox_trans = tk.Text(master=frm_formLeft, height=12,width=40)
txtbox_trans.pack(fill='x', padx=20, pady=5)

# Create the Label and Entry widgets for "Transaction"
lbl_trans_amt = tk.Label(master=frm_transAmt, text="Transaction Amount:")
ent_trans_amt = tk.Entry(master=frm_transAmt,width=20)

lbl_trans_amt.pack(fill='x', padx=5, pady=5, side=tk.LEFT)
ent_trans_amt.pack(fill='x', padx=5, pady=5, side=tk.LEFT)

# button
button = ttk.Button(
    master=frm_formButton,
    text="Process Transaction",
    command=show_selected_size)

button.pack(fill='x', padx=5, pady=5, side=tk.LEFT)

# button
button = ttk.Button(
    master=frm_formButton,
    text="Exit",
    command=window.destroy)

button.pack(fill='x', padx=5, pady=5, side=tk.LEFT)

window.mainloop()