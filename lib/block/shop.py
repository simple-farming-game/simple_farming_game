import pygame
import random

from . import Block
from .. import farm
from ..plants import plants_list

class Shop(Block.Block):
    is_shop_opne: bool = False
    name: str = "shop"
    
    def init(self):
        pass
    
    def interact(self):
        self.is_shop_opne = not self.is_shop_opne
    
    def update(self):
        if self.is_shop_opne:
            print("test")