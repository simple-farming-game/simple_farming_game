import pygame
import random

from . import Plants


class Carrots(Plants.Plants):
    name = "carrots"
    price = 10
    growCount = 0
    age = 0
    maxAge = 2
    water = False
    rotCount = 0
    
    # 이벤트
    GROW_EVENT = pygame.USEREVENT
    
    def __init__(self, pos: pygame.Vector2, screen: pygame.Surface) -> None:
        super().__init__(pos, screen)
        pygame.time.set_timer(self.GROW_EVENT, 10000)
    
    def grow(self):
        if self.water:
            self.growCount += random.randint(0, 10)
            if (self.growCount < 10000) and (self.age):
                self.update_image(
                    pygame.image.load(f"assets/img/plants/{self.name}/farm_0.png")
                )
            if (self.growCount >= 10000) and (self.age == 0):
                self.update_image(
                    pygame.image.load(f"assets/img/plants/{self.name}/farm_1.png")
                )
                self.age += 1
                self.water = False
            if (self.growCount >= 25000) and (self.age == 1):
                self.update_image(
                    pygame.image.load(f"assets/img/plants/{self.name}/farm_2.png")
                )
                self.age += 1
                self.water = False

    def rot(self):
        if self.rotCount >= 10000:
            return True
        if self.water == False:
            self.rotCount += random.randint(0, 5)
