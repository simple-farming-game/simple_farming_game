from lib.blocks.Blocks import Blocks
from lib.blocks.shop import shop_gui
import pygame
from typing import Union


class Shop(Blocks):
    name: str = "shop"
    price: int = 100
    image: pygame.Surface
    age: int
    is_active: bool = False

    def __init__(
        self,
        tile_pos: pygame.Vector2,
        screen: pygame.Surface,
    ) -> None:
        shop_gui.init()

        from lib.runtime_values import SKYBLUE

        self.SKYBLUE = SKYBLUE

        super().__init__(tile_pos, screen)

    def use(self):
        self.is_active = not self.is_active
        print(self.is_active)
        return super().use()

    def update(self):
        if self.is_active:
            shop_gui.open_shop(self.SKYBLUE)
        return super().update()
