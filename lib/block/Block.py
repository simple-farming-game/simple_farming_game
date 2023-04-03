from ..Object import Object
import pygame

class Block(Object):
    name: str  # 영어로 적고 lang 파일에서 참조.

    def __init__(self, pos: pygame.math.Vector2, screen: pygame.Surface) -> None:
        image = pygame.image.load(f"assets/img/block/{self.name}.png")
        super().__init__(image, pos, screen)