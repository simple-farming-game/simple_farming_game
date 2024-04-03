from enum import Enum, auto
import pygame
from lib import runtime_values
from lib import item
from lib import farm
from math import trunc
from lib.crops.crops_item import CropsItems
from lib.crops.Crops import Crops
from lib import runtime_values
import os


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


class Player:
    gold: int = 0
    inventory: list[item.Item] = []
    pos: pygame.Vector2 = pygame.Vector2(0, 0)
    handle_item: item.Items | CropsItems = item.Items.NONE
    # 방향 구하기 (x2−x1,y2−y1)
    # (1,0) <
    # (-1,0) >
    # (0,1) ^

    def __init__(self, img: pygame.Surface, pos: pygame.Vector2, speed: int) -> None:
        self.img: pygame.Surface = img
        self.pos: pygame.Vector2 = pos
        self.speed: float = speed

    def draw(self):
        runtime_values.screen.blit(self.img, self.pos)

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

    def tile_pos(self):
        return self.pos // 32

    def farm_tile(self, pos):
        x, y = map(int, pos)
        if (
            self.handle_item == item.Items.HOE
            and not farm.tile_map[x][y] == farm.Tiles.FARMLAND
        ):
            farm.tile_map[x][y] = farm.Tiles.FARMLAND

    def harvest_crops(self, pos):
        x, y = map(int, pos)
        if (
            self.handle_item == item.Items.SICKLE
            and isinstance(farm.tile_map[x][y], Crops)
            and farm.tile_map[x][y].age == 2
        ):
            try:
                inventory_copy = self.inventory[:]
                while item.Items.NONE in inventory_copy:
                    inventory_copy.remove(item.Items.NONE)
                for i in CropsItems:
                    if farm.tile_map[x][y].name.upper() == i.name:
                        self.inventory[len(inventory_copy)] = i
                farm.tile_map[x][y] = farm.Tiles.FARMLAND
            except IndexError:
                pass

    def plant_crops(self):
        # telnetover9000
        x, y = map(int, self.tile_pos())
        if isinstance(self.handle_item, CropsItems):
            farm.tile_map[x][y] = self.handle_item.value(
                self.tile_pos(), runtime_values.screen
            )
