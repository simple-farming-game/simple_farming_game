import pygame
from .types.Image import Image


class Object:
    image: Image

    def __init__(self, image: Image, pos: pygame.math.Vector2, screen: pygame.Surface) -> None:
        self.image = image
        self.pos = pos
        self.screen = screen

    def update_image(self, image: Image):
        self.image = image

    def draw(self) -> None:
        self.screen.blit(self.image.image, self.pos)

    # def draw_tiled(self) -> None:
    #     self.screen.blit(
    #         self.image.image,
    #         pygame.math.Vector2(
    #             self.pos.x,
    #             self.pos.y
    #         )
    #     )
