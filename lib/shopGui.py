import tkinter

root = tkinter.Tk()

root.title("Shop")
root.geometry("300x300")

def init(plants_list, block_list):
    from lib import sell

    for j, i in enumerate(plants_list+block_list):
        nameLabel = tkinter.Label(root, text=i.name)
        nameLabel.grid(row=j, column=0)
        countLabel = tkinter.Button(root, text=f"구매", command=sell.buy(i.name))
        countLabel.grid(row=j, column=1)

def shop_opne():
    root.mainloop()