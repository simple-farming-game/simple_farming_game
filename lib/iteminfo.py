import tkinter
from lib import runtime_values

def info(select, itemCount):
    root = tkinter.Tk()
 
    nameLabel = tkinter.Label(root, text=f"{runtime_values.lang['name']} : {select}")
    nameLabel.grid(row=0, column=0)
    countLabel = tkinter.Label(root, text=f"{runtime_values.lang['count']} : {itemCount}")
    countLabel.grid(row=1, column=0)

    root.mainloop()