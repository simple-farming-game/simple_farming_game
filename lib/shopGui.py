import tkinter

root = tkinter.Tk()

root.title("Shop")
root.geometry("300x300")

def shop_opne(plants_list, block_list):
    for j, i in enumerate(plants_list.plants_list+block_list.block_list):
        nameLabel = tkinter.Label(root, text=i.name)
        nameLabel.grid(row=j, column=0)
        countLabel = tkinter.Button(root, text=f"구매")
        countLabel.grid(row=j, column=1)


    root.mainloop()