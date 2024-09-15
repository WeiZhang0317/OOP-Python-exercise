import tkinter as tk

window = tk.Tk()
window.title('My Window')
window.geometry('300x100')
 
l = tk.Label(window, bg='white', width=20, text='empty')
l.pack(fill=tk.X)
 
def print_selection():
    if (var1.get() == 1) & (var2.get() == 0):
        l.config(text='I love Python ')
    elif (var1.get() == 0) & (var2.get() == 1):
        l.config(text='I love Java')
    elif (var1.get() == 0) & (var2.get() == 0):
        l.config(text='I do not love anything')
    else:
        l.config(text='I love both')

# Create Frame widget
new_frame = tk.Frame(window, width=200, height=400)
new_frame.pack()

var1 = tk.IntVar()
var2 = tk.IntVar()
c1 = tk.Checkbutton(new_frame, text='Python',variable=var1, onvalue=1, offvalue=0, command=print_selection)
c1.pack(fill=tk.X, padx=10, side=tk.LEFT)
c2 = tk.Checkbutton(new_frame, text='Java',variable=var2, onvalue=1, offvalue=0, command=print_selection)
c2.pack(fill=tk.X, padx=10, side=tk.LEFT)
 
window.mainloop()