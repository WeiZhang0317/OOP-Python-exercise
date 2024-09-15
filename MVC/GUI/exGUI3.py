from tkinter import *

root = Tk()
root.title("Tk Example")
root.minsize(200, 200)  # width, height
root.geometry("300x300+50+50")

# Create Label in our window
text = Label(root, text="Welcome to COMP642")
text.pack() # placing the widget to the parent window
text2 = Label(root, text="This is my first tkinter program")
text2.pack()
root.mainloop()