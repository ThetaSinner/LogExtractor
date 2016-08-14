""" Sandpit GUI """

import sys
from tkinter import *
from tkinter import ttk
from tkinter import filedialog


def onClick(event):
    print("Clicked")


def main():
    root = Tk()
    root.title("Log Extractor")
    root.geometry("500x500")
    root.bind("<Escape>", lambda event: root.destroy())

    mainframe = ttk.Frame(root, padding="3 3 3 3")
    mainframe.grid(column=0, row=0)

    ttk.Label(mainframe, text="my button").grid(row=0, column=0, sticky=W)

    button = ttk.Button(mainframe, text="Hello World")
    button.bind("<Button-1>", onClick)
    button.grid(row=0, column=1)

    nameInputLabel = ttk.Label(mainframe, text="name")
    nameInputLabel.grid(row=1, column=0, sticky=W)

    name = StringVar()
    nameInput = ttk.Entry(mainframe, textvariable=name)
    nameInput.grid(row=1, column=1)

    nameSubmit = ttk.Button(mainframe, text="submit")
    nameSubmit.bind("<Button-1>", lambda event: print(name.get()))
    nameSubmit.grid(row=1, column=2)

    selectVar = StringVar()
    select = ttk.Combobox(mainframe, textvariable=selectVar)
    select['values'] = ("thing", "stuff")
    select.state(["readonly"])
    select.grid(row=2, column=0)

    ttk.Button(mainframe, text="bl").grid(row=3, column=3, sticky=(S, E))

    filedialog.askdirectory()

    filedialog.askopenfilename()

    root.mainloop()


main()
