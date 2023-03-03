import pygame
import random
from .plants_data import Plants, Plants_data
from ..types.Image import Image


class rice(Plants):
    name = "rice"
    growCount = 0
    age = 0

    def __init__(self, image: Image, pos: pygame.math.Vector2, screen: pygame.Surface, plants_data: Plants_data) -> None:
        super().__init__(image, pos, screen, plants_data)

    def grow(self, growCount):
        self.growCount += random.randint(0, growCount)
        if (self.growCount >= 10000) and (self.age == 0):
            self.update_image(
                Image(pygame.image.load("assets/img/farm_rice_1.png")))
            self.age = 1
        if (self.growCount >= 25000) and (self.age == 1):
            self.update_image(
                Image(pygame.image.load("assets/img/farm_rice_2.png")))
            self.age = 2
