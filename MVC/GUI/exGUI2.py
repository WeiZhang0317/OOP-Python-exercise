from tkinter import *

root = Tk()  # create the main window
root.title("Tk Example")  #title of the window
root.configure(background="yellow") #set window's background to yellow
root.minsize(200, 200)  # set the minimum width, height
root.maxsize(500, 500)  # set the maximum width and height
root.geometry("300x300+50+50")  # width x height + x + y - placement of the window
root.mainloop()