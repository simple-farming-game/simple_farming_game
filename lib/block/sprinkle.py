import pygame
import random

from . import Block
from .. import farm
from ..plants import plants_list
class Sprinkle(Block.Block):
    vitamin: bool = False
    name:str = "sprinkle"
    rangeList:list[list[int]] = []
    
    def water(self):
        print("helo")
        for j in range(0,3):
            self.rangeList.append([])
            for i in range(-2,4):
                self.rangeList[j].append(int(super().pos.x//32 + i))
                self.rangeList[j].append(int(super().pos.y//32 + i))
        for i in self.rangeList:
            if farm.tileMap[i[0]][i[1]] in plants_list.plants_list:
                farm.tileMap[i[0]][i[1]].water = True # type: ignore