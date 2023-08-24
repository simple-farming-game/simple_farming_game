import pygame

btn_list = []

def init(plants_list, block_list):
    from lib.lang import text
    from lib import ui
    btn_y = 0
    index = 1
    for item in plants_list:
        btn_list.append(ui.Btn(f"{index}. {text(f'items.{item.name}')}", lambda: buy(item.name), pygame.math.Vector2(50,btn_y)))
        index+=1
        btn_y+=50
    for item in block_list:
        btn_list.append(ui.Btn(f"{index}. {text(f'blocks.{item.name}')}", lambda: buy(item.name), pygame.math.Vector2(50,btn_y)))
        index+=1
        btn_y+=50

def buy(name):
    from lib import sell

    sell.buy(name)

def shop_open():
    for btn in btn_list:
        btn.draw()