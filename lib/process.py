from lib import farm
from lib import runtime_values
from lib.block import block_list
import pygame

def process():
    runtime_values.players[0].update()
    tilePos = pygame.math.Vector2(0, 0)
    for line in farm.tileMap:
        for tile in line:
            if isinstance(tile, block_list.block_list[0]):  # type: ignore
                tile.water() # type: ignore
            tilePos.y += 32
        tilePos.x += 32
        tilePos.y = 0