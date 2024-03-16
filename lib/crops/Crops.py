import pygame
from typing import Final


class Crops:
    name: str
    image: pygame.Surface
    age: int
    GROW_EVENT = pygame.USEREVENT

    def __init__(self, tile_pos: pygame.Vector2, screen: pygame.Surface) -> None:
        self.screen = screen
        self.tile_pos: Final = pygame.Vector2(tile_pos[0], tile_pos[1])
        self.age = 0
        pygame.time.set_timer(self.GROW_EVENT, 10000)

    def draw(self):
        self.image = pygame.image.load(
            f"./assets/img/plants/{self.name}/farm_{self.age}.png"
        )
        self.screen.blit(self.image, self.tile_pos * 32)

    def grow(self):
        if not self.age >= 2:
            self.age += 1
