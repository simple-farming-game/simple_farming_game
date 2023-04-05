from lib import farm
from lib.block import block_list
import pygame
import lib.runtime_values as rv

def process():
    tilePos = pygame.math.Vector2(0, 0)
    for line in farm.tileMap:
        for tile in line:
            if isinstance(tile, block_list.block_list[1]):  # type: ignore
                tile.water(rv.screen) # type: ignore
            tilePos.y += 32
        tilePos.x += 32
        tilePos.y = 0