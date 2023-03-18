import pygame

from ..object import Object


class Plants(Object):
    name: str  # 영어로 적고 lang 파일에서 참조.
    price: int
    maxAge: int

    def __init__(self, pos: pygame.math.Vector2, screen: pygame.Surface) -> None:
        image = pygame.image.load(f"assets/img/plants/{self.name}/farm_0.png")
        super().__init__(image, pos, screen)
        self.age: int
        self.watered: bool
        self.rotCount: int

    def grow(self) -> None: ...
    def rot(self) -> None: ...
