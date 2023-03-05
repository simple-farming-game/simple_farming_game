import pygame
import random

from . import Plants


class rice(Plants.Plants):
    name = "rice"
    price = 10
    growCount = 0
    age = 0
    maxAge = 2

    def grow(self, growCount):
        self.growCount += random.randint(0, growCount)
        if (self.growCount < 10000) and (self.age):
            self.update_image(
                pygame.image.load("assets/img/rice/farm_0.png"))
        if (self.growCount >= 10000) and (self.age == 0):
            self.update_image(
                pygame.image.load("assets/img/rice/farm_1.png"))
            self.age = 1
        if (self.growCount >= 25000) and (self.age == 1):
            self.update_image(
                pygame.image.load("assets/img/farm_rice_2.png"))
            self.age = 2
