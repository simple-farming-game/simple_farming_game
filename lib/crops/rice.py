from lib.crops.Crops import Crops
import pygame

class Rice(Crops):
    tile_pos: pygame.Vector2
    name: str = "rice"
    image: pygame.Surface
    age: int
    def __init__(self, tile_pos: pygame.Vector2, screen: pygame.Surface) -> None:
        super().__init__(tile_pos, screen)
        