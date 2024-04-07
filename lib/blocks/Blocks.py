import pygame
import json
from typing import Final
import random


class Blocks:
    name: str
    image: pygame.Surface

    def __init__(
        self,
        tile_pos: pygame.Vector2,
        screen: pygame.Surface,
    ) -> None:
        self.screen = screen
        self.tile_pos: Final = pygame.Vector2(tile_pos[0], tile_pos[1])

    def draw(self):
        self.image = pygame.image.load(f"./assets/img/block/{self.name}.png")
        self.screen.blit(self.image, self.tile_pos * 32)

    def update(self):
        pass
