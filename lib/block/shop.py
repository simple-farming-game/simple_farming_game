import pygame
import random

from . import Block
from .. import draw

class Shop(Block.Block):
    name:str = "shop"
    shop_opne = False
    
    def init(self):
        pass
    
    def interact(self):
        self.shop_opne = not self.shop_opne

    def update(self, runtime_values):
        if self.shop_opne:
            draw.draw_text_with_border( # 돈
                runtime_values.screen, runtime_values.font,
                "상점입니다",
                runtime_values.WHITE, runtime_values.BLACK, 2, pygame.math.Vector2(10,10))