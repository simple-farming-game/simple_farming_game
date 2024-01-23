from lib.crops.Crops import Crops
import pygame
from typing import Union

class Rice(Crops):
    name: str = "rice"
    image: pygame.Surface
    age: int
    def __init__(self, tile_pos: pygame.Vector2, screen: pygame.Surface, path: Union[str, None]) -> None:
        super().__init__(tile_pos, screen, path)
        