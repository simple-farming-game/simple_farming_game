import pygame
import random

from . import Block
from .. import farm
from ..plants import plants_list

class Shop(Block.Block):
    vitamin: bool = False
    name:str = "shop"
    rangeList:list = []
    
    def init(self):
        pass
    
    def interact(self):
        print("shop")