import pygame


class Object:
    image: pygame.Surface

    def __init__(
        self, image: pygame.Surface, pos: pygame.math.Vector2, screen: pygame.Surface
    ) -> None:
        self.image = image
        self.pos = pos
        self.screen = screen

    def update_image(self, image: pygame.Surface):
        self.image = image

    def draw(self) -> None:
        self.screen.blit(self.image, self.pos)
