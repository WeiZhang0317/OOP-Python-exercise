import tkinter as tk

root = tk.Tk()

v = tk.StringVar()
v.set("Python")  # initializing the choice, i.e. Python

languages = ["Python", "Perl", "Java", "C++", "C"]

def ShowChoice():
    print(v.get())

tk.Label(root, text="Choose your favourite programming language:", justify = tk.LEFT, padx = 20).pack()

for language in languages:
    tk.Radiobutton(root, text=language, padx = 20, variable=v, command=ShowChoice, value=language).pack(anchor=tk.W)


root.mainloop()