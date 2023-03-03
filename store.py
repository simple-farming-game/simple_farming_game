import tkinter
import json
import main
with open('data/price_tag.json') as f:
    price = json.load(f)


def sail(item, number):
    print(item, number)
    playerClass = main.playerClass
    if playerClass.inventory[item] >= number:
        playerClass.inventory[item] -= number
        playerClass.inventory["gold"] -= price[item]*number
    else:
        print("겟수가 부족합니다")
