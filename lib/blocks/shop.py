from lib.blocks.Blocks import Blocks
import pygame
from typing import Union


class Shop(Blocks):
    name: str = "shop"
    image: pygame.Surface
    age: int

    def __init__(
        self,
        tile_pos: pygame.Vector2,
        screen: pygame.Surface,
    ) -> None:
        super().__init__(tile_pos, screen)
