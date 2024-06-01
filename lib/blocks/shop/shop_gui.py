import pygame
from lib import ui
from lib.crops.crops_item import CropsItems
from lib import trade

buy_btns = []
sell_btns = []


def init():
    from lib.runtime_values import screen
    from lib.runtime_values import font

    for index, item in enumerate(CropsItems):
        buy_btns.append(
            ui.Btn(
                f"{item.name} Gold: {item.value.price} Buy!",
                lambda: trade.buy(item),
                pygame.math.Vector2(10, (10 + 25 * index) * 4),
                screen,
                font,
            )
        )
        sell_btns.append(
            ui.Btn(
                f"Sell!",
                lambda: trade.sell(item),
                pygame.math.Vector2(10, (10 + 25 * index) * 6 + 10),
                screen,
                font,
            )
        )


def open_shop(background_color: pygame.Color):
    from lib.runtime_values import screen

    screen.fill(background_color)

    for i in buy_btns:
        i.draw()
    for i in sell_btns:
        i.draw()
