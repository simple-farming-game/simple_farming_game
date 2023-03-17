from enum import Enum, auto
from typing import List, Union

import lib.plants.plants_list as plants_list

class Tiles(Enum):
    DIRT = auto()
    FARMLAND = auto()
    WATER_FARMLAND = auto()


tileMap: List[List[Union[Tiles, plants_list.plants_type]]] = [
    [Tiles.DIRT for _ in range(20)] for _ in range(30)]


def grow_plants():
    for line in tileMap:
        for tile in line:
            if isinstance(tile, plants_list.plants_list):  # type: ignore
                tile.grow()  # type: ignore

def rot_plants(runtime_values):
    tilePos = [0,0]
    for line in tileMap:
        for tile in line:
            if isinstance(tile, plants_list.plants_list):  # type: ignore
                if tile.rot(): # type: ignore
                    tileMap[tilePos[0]][tilePos[1]] = Tiles.FARMLAND
                    runtime_values.logs.info(f"rot plant: {tile.name} pos: {tilePos}")
            tilePos[1] +=1
        tilePos[0] += 1
        tilePos[1] = 0