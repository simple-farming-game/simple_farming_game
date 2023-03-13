import pygame
import random

from . import Plants


class Rice(Plants.Plants):
    name = "rice"
    price = 10
    growCount = 0
    age = 0
    maxAge = 2

    def grow(self):
        self.growCount += random.randint(-3, 5)
        if (self.growCount < 10000) and (self.age):
            self.update_image(
                pygame.image.load(f"assets/img/plants/{self.name}/farm_0.png"))
        if (self.growCount >= 10000) and (self.age == 0):
            self.update_image(
                pygame.image.load(f"assets/img/plants/{self.name}/farm_1.png"))
            self.age = 1
        if (self.growCount >= 25000) and (self.age == 1):
            self.update_image(
                pygame.image.load(f"assets/img/plants/{self.name}/farm_2.png"))
            self.age = 2
