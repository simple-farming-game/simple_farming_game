import pygame

from ..Object import Object


class Plants(Object):
    name: str  # 영어로 적고 lang 파일에서 참조.

    def __init__(self, image: pygame.Surface, pos: pygame.math.Vector2, screen: pygame.Surface) -> None:
        super().__init__(image, pos, screen)

    def grow(self) -> None: ...
