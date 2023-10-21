from enum import Enum, auto
from typing import Dict, Union
import pygame
import random

from lib.Object import Object
from lib.plants import plants_list
from lib.farm import *
from lib import items
from lib.block import block_list


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
    NONE = auto()


class player(Object):
    speed: float = 3
    inventory: Dict[str, int] = {"sprinkle": 100}
    inventory_size: int = 8
    gold: int = 50
    handle_item: Union[
        plants_list.plants_type, block_list.block_type, items.Items
    ] = items.Items.NONE

    def __init__(
        self,
        image: pygame.Surface,
        pos: pygame.math.Vector2,
        screen: pygame.Surface,
        window_size,
    ) -> None:
        super().__init__(image, pos, screen)
        self.window_size = window_size

        for i in items.value_name:
            self.inventory[f"{i}"] = 1

    def update(self):
        for key, value in dict(self.inventory).items():
            if value == 0:
                del self.inventory[key]
                self.handle_item = items.Items.NONE

    def move(self, direction: Direction, frame):
        match direction:
            case Direction.LEFT:
                self.pos.x += -self.speed + frame
            case Direction.RIGHT:
                self.pos.x += self.speed + frame
            case Direction.UP:
                self.pos.y += -self.speed + frame
            case Direction.DOWN:
                self.pos.y += self.speed + frame
            case Direction.UP_LEFT:
                self.pos.x += -self.speed + frame
                self.pos.y += -self.speed + frame
            case Direction.UP_RIGHT:
                self.pos.x += self.speed + frame
                self.pos.y += -self.speed + frame
            case Direction.DOWN_LEFT:
                self.pos.x += -self.speed + frame
                self.pos.y += self.speed + frame
            case Direction.DOWN_RIGHT:
                self.pos.x += self.speed + frame
                self.pos.y += self.speed + frame

        if self.pos.x >= self.window_size[0] - 32:
            self.pos.x = self.window_size[0] - 32
        if self.pos.x <= 0:
            self.pos.x = 0
        if self.pos.y >= self.window_size[1] - 32:
            self.pos.y = self.window_size[1] - 32
        if self.pos.y <= 1:
            self.pos.y = 1

    def get_tile_pos(self) -> pygame.math.Vector2:
        return self.pos // 32

    def farm_plant(self):
        tPos = self.get_tile_pos()
        tile = tileMap[int(tPos.x)][int(tPos.y)]
        if isinstance(tile, plants_list.plants_list):  # type: ignore
            if tile.maxAge == tile.age:  # type: ignore
                try:
                    self.inventory[tile.name] += random.randint(1, 4)
                    self.inventory[f"{tile.name}_seed"] += random.randint(1, 3)
                except KeyError:
                    self.inventory[tile.name] = random.randint(1, 4)
                    self.inventory[f"{tile.name}_seed"] = random.randint(1, 3)

                tileMap[int(tPos.x)][int(tPos.y)] = Tiles.FARMLAND

    def plant_plant(self, screen: pygame.Surface) -> bool:
        tPos = self.get_tile_pos()

        # check self
        if not self.handle_item in plants_list.plants_list:
            return False
        if self.inventory[f"{self.handle_item.name}_seed"] <= 0:
            return False

        # check farm empty
        if not tileMap[int(tPos.x)][int(tPos.y)] == Tiles.FARMLAND:
            return False

        self.inventory[f"{self.handle_item.name}_seed"] -= 1
        tileMap[int(tPos.x)][int(tPos.y)] = self.handle_item(
            tilePosToPos(tPos), screen
        )  # type: ignore
        return True

    def put_block(self, screen: pygame.Surface) -> bool:
        tPos = self.get_tile_pos()

        # check self
        if not self.handle_item in block_list.block_list:
            return False
        if self.inventory[f"{self.handle_item.name}"] == 0:
            return False

        # check farm empty
        if not tileMap[int(tPos.x)][int(tPos.y)] == Tiles.DIRT:
            return False

        self.inventory[f"{self.handle_item.name}"] += -1
        tileMap[int(tPos.x)][int(tPos.y)] = self.handle_item(
            tilePosToPos(tPos), screen
        )  # type: ignore
        return True


def tilePosToPos(tilePos: pygame.math.Vector2) -> pygame.math.Vector2:
    return pygame.math.Vector2(tilePos[0] * 32, tilePos[1] * 32)
