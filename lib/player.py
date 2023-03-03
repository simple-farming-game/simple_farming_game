import math
from typing import Dict
import pygame

from lib.types.Direction import Direction
from lib.types.Image import Image
from lib.Object import Object


class player(Object):
    speed = 1
    inventory: Dict[str, int]

    def __init__(self, image: Image, pos: pygame.math.Vector2, screen: pygame.Surface, window_size) -> None:
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
