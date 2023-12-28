from enum import Enum, auto
from typing import Dict, Union
import pygame
from lib import runtime_values
from lib import item
from lib import farm
from math import trunc
from lib.crops.Crops import Crops
from lib.crops.crops_item import CropsItem

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
    inventory: list[Union[item.Items, CropsItem]] = []
    pos: pygame.Vector2 = pygame.Vector2(0,0)
    hendle_item = item.Items.NONE
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
        if self.hendle_item == item.Items.HOE:
            farm.tile_map[x][y] = farm.Tiles.FARMLAND
    
    def plant_crops(self):
        #telnetover9000
        x, y = map(int, self.tile_pos())
        if isinstance(self.hendle_item, CropsItem):
            farm.tile_map[x][y] = self.hendle_item.value