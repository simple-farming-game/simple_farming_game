from enum import Enum, auto
from typing import List, Union

# Importing the plants_list module from the lib.plants package
import lib.plants.plants_list as plants_list

# Defining an enumeration class for the different tile types
class Tiles(Enum):
    DIRT = auto()
    FARMLAND = auto()

# Creating a two-dimensional list to represent the game map, with each tile initialized to DIRT
tileMap: List[List[Union[Tiles, plants_list.plants_type]]] = [
    [Tiles.DIRT for _ in range(20)] for _ in range(30)]

# Defining a function to simulate plant growth on the tile map
def grow_plants():
    # Iterating over each row in the tile map
    for line in tileMap:
        # Iterating over each tile in the row
        for tile in line:
            # Checking if the tile is a plant by checking if it is an instance of the plants_list class
            if isinstance(tile, plants_list.plants_list):  # type: ignore
                # If the tile is a plant, calling its grow() method to simulate growth
                tile.grow()  # type: ignore
