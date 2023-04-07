from lib import farm
from lib.block import block_list
<<<<<<< HEAD
import pygame

def process():
    tilePos = pygame.math.Vector2(0, 0)
    for line in farm.tileMap:
        for tile in line:
            if isinstance(tile, block_list.block_list[1]):  # type: ignore
                tile.water() # type: ignore
            tilePos.y += 32
        tilePos.x += 32
        tilePos.y = 0
=======

def process():
    for i in farm.tileMap:
        for j in i:
            if j in block_list.block_list:
                j.water()
>>>>>>> 6a6a394 (기능구현 실패)
