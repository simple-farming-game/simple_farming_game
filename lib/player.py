from enum import Enum, auto
import math
from typing import Dict, Union
import pygame
import random

from lib.Object import Object
from lib.plants import plants_list
from lib.farm import tileMap, Tiles
from lib.items import Items

# Define a new enumeration class for player movement directions
class Direction(Enum):
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()
    STOP = auto()
    UP_LEFT = auto()
    UP_RIGHT = auto()
    DOWN_LEFT = auto()
    DOWN_RIGHT = auto()

# Define the player class, which inherits from the Object class
class player(Object):
    speed: float = 3 # Set the player's default speed
    inventory: Dict[str, int] = {} # Initialize the player's inventory as a dictionary
    handle_item: Union[plants_list.plants_type, Items] = Items.NONE # Initialize the item that the player is currently handling as "NONE"

    def __init__(self, image: pygame.Surface, pos: pygame.math.Vector2, screen: pygame.Surface, window_size) -> None:
        super().__init__(image, pos, screen) # Call the superclass's constructor
        self.window_size = window_size # Save the size of the game window

        # Initialize the player's inventory
        for plant in plants_list.plants_list:
            self.inventory[f"{plant.name}"] = 10
            self.inventory[f"{plant.name}_seed"] = 10

    def move(self, direction: Direction, frame):
        # Move the player's position based on the given direction and the current frame number
        match direction:
            case Direction.LEFT:
                self.pos.x += -self.speed+frame
            case Direction.RIGHT:
                self.pos.x += self.speed+frame
            case Direction.UP:
                self.pos.y += -self.speed+frame
            case Direction.DOWN:
                self.pos.y += self.speed+frame
            case Direction.UP_LEFT:
                self.pos.x += -self.speed+frame
                self.pos.y += -self.speed+frame
            case Direction.UP_RIGHT:
                self.pos.x += self.speed+frame
                self.pos.y += -self.speed+frame
            case Direction.DOWN_LEFT:
                self.pos.x += -self.speed+frame
                self.pos.y += self.speed+frame
            case Direction.DOWN_RIGHT:
                self.pos.x += self.speed+frame
                self.pos.y += self.speed+frame

        # Keep the player's position within the bounds of the game window
        if self.pos.x >= self.window_size[0]-32:
            self.pos.x = self.window_size[0]-33
        if self.pos.x <= 0:
            self.pos.x = 1
        if self.pos.y >= self.window_size[1]-32:
            self.pos.y = self.window_size[1]-32
        if self.pos.y <= 1:
            self.pos.y = 1

    def get_tile_pos(self) -> pygame.math.Vector2:
        # Calculate the position of the tile that the player is currently standing on
        return pygame.math.Vector2(
            math.trunc(self.pos.x/32),
            math.trunc(self.pos.y/32)
        )

    def farm_plant(self):
        # Harvest a plant that the player is standing on and update their inventory
        tPos = self.get_tile_pos()
        tile = tileMap[int(tPos.x)][int(tPos.y)]
        if isinstance(tile, plants_list.plants_list):  # type: ignore
            if tile.maxAge == tile.age:  # type: ignore
                # Increase inventory by random amount between 0 and 4, and add a seed of the harvested plant
                self.inventory[tile.name] += random.randint(0, 4)
                self.inventory[f"{tile.name}_seed"] += 1
                # Replace the harvested plant with farmland
                tileMap[int(tPos.x)][int(tPos.y)] = Tiles.FARMLAND

    def plant_plant(self, screen: pygame.Surface) -> bool:
        tPos = self.get_tile_pos()

        # check if plant is valid
        if not self.handle_item in plants_list.plants_list:
            return False
        # check if player has seeds of this plant
        if self.inventory[f"{self.handle_item.name}_seed"] == 0:
            return False

        # check if farm tile is empty
        if not tileMap[int(tPos.x)][int(tPos.y)] == Tiles.FARMLAND:
            return False

        # reduce seed count in inventory
        self.inventory[f"{self.handle_item.name}_seed"] += -1

        # place plant in the farm tile
        tileMap[int(tPos.x)][int(tPos.y)] = self.handle_item(
            tilePosToPos(tPos), screen)  # type: ignore

        return True


    def tilePosToPos(tilePos: pygame.math.Vector2) -> pygame.math.Vector2:
        # convert tile position to screen position
        return pygame.math.Vector2(tilePos[0]*32, tilePos[1]*32)
