from enum import Enum, auto
import math
from typing import Dict
import pygame

from .Object import Object
# from lib.farm import tileMap, Plants_type, Tiles


class Direction(Enum):
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()
    STOP = auto()


class player(Object):
    speed = 1
    inventory: Dict[str, int] = {}

    def __init__(self, image: pygame.Surface, pos: pygame.math.Vector2, screen: pygame.Surface, window_size) -> None:
        super().__init__(image, pos, screen)
        self.window_size = window_size

    def move(self, direction: Direction):
        match direction:
            case Direction.LEFT:
                self.pos.x -= self.speed
            case Direction.RIGHT:
                self.pos.x += self.speed
            case Direction.UP:
                self.pos.y -= self.speed
            case Direction.DOWN:
                self.pos.y += self.speed

        if self.pos.x >= self.window_size[0]-32:
            self.pos.x = self.window_size[0]-33
        if self.pos.x <= 0:
            self.pos.x = 1
        if self.pos.y >= self.window_size[1]-32:
            self.pos.y = self.window_size[1]-32
        if self.pos.y <= 1:
            self.pos.y = 1

    def get_tile_pos(self) -> pygame.math.Vector2:
        return pygame.math.Vector2(
            math.trunc(self.pos.x/32),
            math.trunc(self.pos.y/32)
        )

    def farm_plant(self):
        tPos = self.get_tile_pos()
        tile = tileMap[int(tPos.x)][int(tPos.y)]
        if tile in Plants_type:
            self.inventory[tile.name] += 1
            self.inventory[f"{tile.name}_seed"] += 1
            tileMap[int(tPos.x)][int(tPos.y)] = Tiles.FARMLAND
