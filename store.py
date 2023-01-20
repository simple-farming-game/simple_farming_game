import tkinter
import json
import main
with open('data/price_tag.json') as f:
    price = json.load(f)


def sail(item, number):
    playerClass = main.playerClass
    if playerClass.inventory[item] >= number:
        playerClass.inventory[item] -= number
        playerClass.inventory["gold"] -= price["rice"]*number


def store():
    main = tkinter.Tk()
    main.title("스토어")
    main.mainloop()


store()
