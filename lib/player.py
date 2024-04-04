from enum import Enum, auto
import pygame
from lib import runtime_values
from lib import item
from lib import farm
from math import trunc
from lib.crops.crops_item import CropsItems
from lib.crops.Crops import Crops
from lib import runtime_values
from lib import funcs
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
                found_crop_item = False
                for inventory_item in self.inventory:
                    if isinstance(inventory_item, item.Item) and isinstance(
                        inventory_item.item, CropsItems
                    ):
                        # Check if the inventory item is a crop and matches the harvested crop
                        if (
                            inventory_item.item.name.upper()
                            == farm.tile_map[x][y].name.upper()
                        ):
                            inventory_item.count += 1
                            found_crop_item = True
                            break  # Stop searching once the item is found and count is updated

                # If no matching crop item found in inventory, add one
                if not found_crop_item:
                    last_index = funcs.last_index_except(
                        [i.item for i in self.inventory], item.Items.NONE
                    )
                    self.inventory[last_index + 1] = item.Item(
                        getattr(CropsItems, farm.tile_map[x][y].name.upper()), 1
                    )

                farm.tile_map[x][y] = farm.Tiles.FARMLAND
            except IndexError:
                pass

    def plant_crops(self):
        # telnetover9000
        x, y = map(int, self.tile_pos())
        print(runtime_values.select_inventory)
        if (
            isinstance(self.handle_item, CropsItems)
            and not self.inventory[runtime_values.select_inventory].count <= 0
        ):
            farm.tile_map[x][y] = self.handle_item.value(
                self.tile_pos(), runtime_values.screen
            )
            self.inventory[runtime_values.select_inventory].count -= 1
            print(self.inventory[runtime_values.select_inventory].count)
