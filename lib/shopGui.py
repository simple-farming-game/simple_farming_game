import pygame

btn_list = []
btn_y = 0

def init(plants_list, block_list):
    from lib import ui
    global btn_y
    for index, item in enumerate(plants_list + block_list):
        btn_list.append(ui.Btn(f"{index}. {item.name}", lambda: buy(item.name), pygame.math.Vector2(50,btn_y)))
        btn_y+=50

def buy(name):
    from lib import sell

    sell.buy(name)

def shop_open():
    for btn in btn_list:
        btn.draw()