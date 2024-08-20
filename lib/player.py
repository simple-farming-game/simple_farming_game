from enum import Enum, auto
import pygame
from lib import runtime_values
from lib import item
from lib import farm
from math import trunc
from lib.crops.crops_item import CropsItems
from lib.crops.crops_item import crops_item_name_list
from lib.crops.Crops import Crops
from lib.blocks.blocks_item import BlocksItems
from lib.blocks.Blocks import Blocks
from lib import funcs
import os
import random


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
        for index, item_count in enumerate([i.count for i in self.inventory]):
            if item_count <= 0:
                self.inventory[index] = item.Item(item.Items.NONE, 1)  # type: ignore

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

    def add_item(
        self, add_item: item.Items | Crops | Blocks | CropsItems | BlocksItems, count
    ):
        item_inventory = funcs.list_filter(
            [i.item for i in self.inventory], item.Items.NONE
        )
        if isinstance(add_item, Crops):
            add_item = getattr(CropsItems, add_item.name.upper())
        elif isinstance(add_item, Blocks):
            add_item = getattr(BlocksItems, add_item.name.upper())
        try:
            item_index = item_inventory.index(add_item)
        except:
            item_index = -1
        if item_inventory[item_index] == add_item:
            print("dsafsd")
            self.inventory[item_index].count += count
        else:
            self.inventory[len(item_inventory) + 1] = item.Item(add_item, count)

    def del_item(
        self, del_item: item.Items | Crops | Blocks | CropsItems | BlocksItems
    ):
        item_inventory = funcs.list_filter(
            [i.item for i in self.inventory], item.Items.NONE
        )
        if isinstance(del_item, Crops):
            del_item = getattr(CropsItems, del_item.name.upper())
        elif isinstance(del_item, Blocks):
            del_item = getattr(BlocksItems, del_item.name.upper())
        try:
            item_index = item_inventory.index(del_item)
        except:
            runtime_values.logger.error("아이템이 인벤토리에 없습니다.")
            return False
        if item_inventory[item_index] == del_item:
            self.inventory[item_index].count -= 1
            return True
        else:
            runtime_values.logger.error("아이템이 인벤토리에 없습니다.")
            return False

    def tile_pos(self):
        return self.pos // 32

    def farm_tile(self, pos):
        x, y = map(int, pos)
        if (
            self.handle_item == item.Items.HOE
            and farm.tile_map[x][y] == farm.Tiles.DIRT
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
                self.add_item(farm.tile_map[x][y], random.randint(1, 4))

                farm.tile_map[x][y] = farm.Tiles.FARMLAND
            except IndexError:
                pass

    def plant_crops(self):
        # telnetover9000
        x, y = map(int, self.tile_pos())
        if (
            isinstance(self.handle_item, CropsItems)
            and not self.inventory[runtime_values.select_inventory].count <= 0
        ):
            farm.tile_map[x][y] = self.handle_item.value(
                self.tile_pos(), runtime_values.screen
            )
            self.inventory[runtime_values.select_inventory].count -= 1

    def put_block(self):
        # telnetover9000
        x, y = map(int, self.tile_pos())
        if (
            isinstance(self.handle_item, BlocksItems)
            and not self.inventory[runtime_values.select_inventory].count <= 0
        ):
            farm.tile_map[x][y] = self.handle_item.value(
                self.tile_pos(), runtime_values.screen
            )
            self.inventory[runtime_values.select_inventory].count -= 1
