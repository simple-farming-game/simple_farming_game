import pygame
import random

from . import Plants


class SunFlower(Plants.Plants):
    name = "sunFlower"
    price = 15
    maxAge = 2

    def __init__(self, pos: pygame.math.Vector2, screen: pygame.Surface) -> None:
        super().__init__(pos, screen)
        self.age = 0
        self.growCount = 0
        self.watered = False
        self.rotCount = 0

    def grow(self):
        if self.watered:
            self.growCount += random.randint(0, 10)
            if (self.growCount < 10000) and (self.age):
                self.update_image(
                    pygame.image.load(f"assets/img/plants/{self.name}/farm_0.png"))
            if (self.growCount >= 10000) and (self.age == 0):
                self.update_image(
                    pygame.image.load(f"assets/img/plants/{self.name}/farm_1.png"))
                self.age += 1
                self.watered = False
            if (self.growCount >= 25000) and (self.age == 1):
                self.update_image(
                    pygame.image.load(f"assets/img/plants/{self.name}/farm_2.png"))
                self.age += 1
                self.watered = False

    def rot(self):
        if self.rotCount >= 5000:
            return True
        if self.watered == False:
            self.rotCount += random.randint(0, 5)
