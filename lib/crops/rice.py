from lib.crops.Crops import Crops
import pygame
from typing import Union


class Rice(Crops):
    name: str = "rice"
    price: int = 10
    image: pygame.Surface
    age: int

    def __init__(
        self,
        tile_pos: pygame.Vector2,
        screen: pygame.Surface,
        age: int = 0,
        age_count: int = 0,
    ) -> None:
        super().__init__(tile_pos, screen, age, age_count)
