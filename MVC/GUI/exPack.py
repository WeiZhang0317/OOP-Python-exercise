import tkinter as tk

root = tk.Tk()

# no options
# w = tk.Label(root, text="Red Sun", bg="red", fg="white")
# w.pack()
# w = tk.Label(root, text="Green Grass", bg="green", fg="black")
# w.pack()
# w = tk.Label(root, text="Blue Sky", bg="blue", fg="white")
# w.pack()

# fill option
""" w = tk.Label(root, text="Red Sun", bg="red", fg="white")
w.pack(fill=tk.X) #widget as wide as the parent widget
w = tk.Label(root, text="Green Grass", bg="green", fg="black")
w.pack(fill=tk.X)   #widget as wide as the parent widget
w = tk.Label(root, text="Blue Sky", bg="blue", fg="white")
w.pack(fill=tk.X)  #widget as wide as the parent widget """

#external padding horizontally
""" w = tk.Label(root, text="Red Sun", bg="red", fg="white")
w.pack(fill=tk.X, padx=10)
w = tk.Label(root, text="Green Grass", bg="green", fg="black")
w.pack(fill=tk.X, padx=10)
w = tk.Label(root, text="Blue Sky", bg="blue", fg="white")
w.pack(fill=tk.X, padx=10) """

""" # external padding horizontally
w = tk.Label(root, text="Red Sun", bg="red", fg="white")
w.pack(fill=tk.X, pady=10)
w = tk.Label(root, text="Green Grass", bg="green", fg="black")
w.pack(fill= tk.X, pady=10)
w = tk.Label(root, text="Blue Sky", bg="blue", fg="white")
w.pack(fill=tk.X, pady=10)  """

""" #internal padding horizontally
w = tk.Label(root, text="Red Sun", bg="red", fg="white")
w.pack()
w = tk.Label(root, text="Green Grass", bg="green", fg="black")
w.pack(ipadx=10)
w = tk.Label(root, text="Blue Sky", bg="blue", fg="white")
w.pack()  """

""" #internal padding vertically
w = tk.Label(root, text="Red Sun", bg="red", fg="white")
w.pack()
w = tk.Label(root, text="Green Grass", bg="green", fg="black")
w.pack(ipadx=10)
w = tk.Label(root, text="Blue Sky", bg="blue", fg="white")
w.pack(ipady=10) """

""" #placing widgets side by side (LEFT)
w = tk.Label(root, text="red", bg="red", fg="white")
w.pack(padx=5, pady=10, side=tk.LEFT)
w = tk.Label(root, text="green", bg="green", fg="black")
w.pack(padx=5, pady=20, side=tk.LEFT)
w = tk.Label(root, text="blue", bg="blue", fg="white")
w.pack(padx=5, pady=20, side=tk.LEFT) """

#placing widgets side by side (RIGHT)
w = tk.Label(root, text="red", bg="red", fg="white")
w.pack(padx=5, pady=10, side=tk.RIGHT)
w = tk.Label(root, text="green", bg="green", fg="black")
w.pack(padx=5, pady=20, side=tk.RIGHT)
w = tk.Label(root, text="blue", bg="blue", fg="white")
w.pack(padx=5, pady=20, side=tk.RIGHT)

tk.mainloop()