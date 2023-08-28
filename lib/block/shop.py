import pygame


from . import Block
from . import block_list
from ..plants import plants_list
from .. import shopGui


class Shop(Block.Block):
    is_shop_opne = False
    name = "shop"
    price = 100

    def init(self):
        shopGui.init(plants_list.plants_list, block_list.block_list)

    def interact(self):
        self.is_shop_opne = not self.is_shop_opne
    
    def update(self):
        if self.is_shop_opne:
            shopGui.shop_open()
