import pygame
from typing import Union, Final

class Crops:
    name: str
    image: pygame.Surface
    age: int
    age_count: int = 0
    
    def __init__(self, tile_pos: pygame.Vector2, screen: pygame.Surface, path: Union[str, None]) -> None:
        if type(path) == str:
            self.image = pygame.image.load(
                f"{path}/assets/img/plants/{self.name}/farm_0.png"
            )
        elif path == None:
            self.image = pygame.image.load(
                f"./assets/img/plants/{self.name}/farm_0.png"
            )
        self.screen = screen
        self.tile_pos: Final = tile_pos
        self.age = 0
    
    def draw(self):
        self.screen.blit(self.image, self.tile_pos*32)
    
    def grow(self, dt):
        if self.age_count >= 20:
            self.age += 1
            self.age_count = 0
        else:
            self.age_count += 1*dt
        