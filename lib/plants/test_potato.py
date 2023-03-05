import pygame
import random

from . import Plants


class potato(Plants.Plants):
    name = "potato"
    growCount = 0
    age = 0

    # def __init__(self, image: pygame.Surface, pos: pygame.math.Vector2, screen: pygame.Surface) -> None:
    #     super().__init__(image, pos, screen)

    def grow(self, growCount):
        self.growCount += random.randint(0, growCount)
        if (self.growCount >= 10000) and (self.age == 0):
            self.update_image(
                pygame.image.load("assets/img/farm_rice_1.png"))
            self.age = 1
        if (self.growCount >= 25000) and (self.age == 1):
            self.update_image(
                pygame.image.load("assets/img/farm_rice_2.png"))
            self.age = 2
