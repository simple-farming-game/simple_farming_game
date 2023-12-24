from enum import Enum, auto
from typing import Dict, Union
import pygame
from lib import runtime_values

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
    inventory: list = []
    pos: pygame.Vector2 = pygame.Vector2(0,0)
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