import pygame

class Crops:
    tile_pos: pygame.Vector2
    name: str
    image: pygame.Surface
    age: int
    age_count: int = 0
    
    def __init__(self, tile_pos: pygame.Vector2, screen: pygame.Surface) -> None:
        self.image = pygame.image.load(
            f"/assets/img/plants/{self.name}/farm_0.png"
        )
        self.screen = screen
        self.tile_pos = tile_pos
        self.age = 0
    
    def draw(self):
        self.screen.blit(self.image, self.tile_pos*32)
    
    def grow(self, dt):
        if self.age_count >= 20:
            self.age += 1
        else:
            self.age_count += 1*dt
        