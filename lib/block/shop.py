import pygame


from . import Block
from . import block_list
from ..plants import plants_list
from .. import shopGui

class Shop(Block.Block):
    is_shop_opne: bool = False
    name: str = "shop"
    price: int = 999999999
    
    def init(self):
        shopGui.init()
    
    def interact(self):
        shopGui.shop_open(block_list.block_list, plants_list.plants_list)