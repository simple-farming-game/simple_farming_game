from enum import Enum, auto
from typing import List, Union

from lib.plants import plants_list
from lib import logger


class Tiles(Enum):
    DIRT = auto()
    FARMLAND = auto()
    WATERED_FARMLAND = auto()


tile_map: List[List[Union[Tiles, plants_list.plants_type]]] = [
    [Tiles.DIRT for _ in range(20)] for _ in range(30)]


def process_plants():
    for x_index, line in enumerate(tile_map):
        for y_index, tile in enumerate(line):
            if isinstance(tile, plants_list.plants_list):  # type: ignore
                tile.grow()  # type: ignore
                if tile.rot():  # type: ignore
                    tile_map[x_index][y_index] = Tiles.FARMLAND
                    logger.log_info(f"rot plant: {tile.name}")
                    logger.log_info(f"pos: {x_index}, {y_index}")
