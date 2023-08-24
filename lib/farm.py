from enum import Enum, auto
from typing import List, Union
import pygame

import lib.plants.plants_list as plants_list
import lib.block.block_list as block_list


class Tiles(Enum):
    DIRT = auto()
    FARMLAND = auto()
    WATER_FARMLAND = auto()


tileMap: List[List[Union[Tiles, plants_list.plants_type]]] = [
    [Tiles.DIRT for _ in range(20)] for _ in range(30)
]


def init():
    import lib.runtime_values as runtime_values

    tileMap[3][3] = block_list.block_list[1](pygame.Vector2(3 * 32, 3 * 32), runtime_values.screen)  # type: ignore

def rot_plants(runtime_values):
    tilePos = [0, 0]
    for line in tileMap:
        for tile in line:
            if isinstance(tile, plants_list.plants_list):  # type: ignore
                if tile.rot():  # type: ignore
                    tileMap[tilePos[0]][tilePos[1]] = Tiles.FARMLAND
                    runtime_values.logs.info(f"rot plant: {tile.name}")
                    runtime_values.logs.info(f"pos: {tilePos}")
            tilePos[1] += 1
        tilePos[0] += 1
        tilePos[1] = 0
