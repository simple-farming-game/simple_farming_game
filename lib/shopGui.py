import tkinter

def init():
    pass

def buy(name):
    from lib import sell
    sell.buy(name)

def shop_open(plants_list, block_list):

    root = tkinter.Tk()

    root.title("Shop")
    root.geometry("300x300")

    for j, i in enumerate(plants_list + block_list):
        nameLabel = tkinter.Label(root, text=i.name)
        nameLabel.grid(row=j, column=0)
        countLabel = tkinter.Button(root, text="구매", command=lambda name=i.name: buy(name))
        countLabel.grid(row=j, column=1)
    
    root.mainloop()
    del root