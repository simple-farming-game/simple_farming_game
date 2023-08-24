import pygame

btn_list = []

def init(plants_list, block_list):
    from lib.lang import text
    from lib import ui
    btn_y = 10
    index = 1
    for item in plants_list:
        btn_list.append(ui.Btn(f"{index}. {text(f'items.{item.name}')}", lambda: buy(item.name), pygame.math.Vector2(10,btn_y)))
        index+=1
        btn_y+=30
    for item in block_list:
        btn_list.append(ui.Btn(f"{index}. {text(f'blocks.{item.name}')}", lambda: buy(item.name), pygame.math.Vector2(10,btn_y)))
        index+=1
        btn_y+=30

def buy(name):
    from lib import sell

    sell.buy(name)

def shop_open():
    from lib.new_screen import background
    from lib.new_screen import color
    background(color.SKYBLUE)
    for btn in btn_list:
        btn.draw()