import pygame
import json
from typing import Final


class Crops:
    name: str
    image: pygame.Surface
    age: int
    age_count: int
    GROW_EVENT = pygame.USEREVENT

    def __init__(
        self,
        tile_pos: pygame.Vector2,
        screen: pygame.Surface,
        age: int = 0,
        age_count: int = 0,
    ) -> None:
        self.screen = screen
        self.tile_pos: Final = pygame.Vector2(tile_pos[0], tile_pos[1])
        self.age = age
        self.age_count = age_count
        pygame.time.set_timer(self.GROW_EVENT, 100)

    def draw(self):
        self.image = pygame.image.load(
            f"./assets/img/plants/{self.name}/farm_{self.age}.png"
        )
        self.screen.blit(self.image, self.tile_pos * 32)

    def grow(self):
        if not self.age >= 2 and not self.age_count >= 100:
            self.age_count += 1
        elif self.age_count >= 100:
            self.age += 1
            self.age_count = 0

    def __str__(self) -> str:
        return json.dumps(
            {
                "name": self.name,
                "age": self.age,
                "age_count": self.age_count,
            }
        )
