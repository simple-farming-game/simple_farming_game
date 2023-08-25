import pygame

from ..Object import Object


class Plants(Object):
    name: str  # 영어로 적고 lang 파일에서 참조.
    price: int
    age: int
    maxAge: int
    water: bool
    rotCount: int

    # 이벤트
    GROW_EVENT = pygame.USEREVENT
    
    def __init__(self, pos: pygame.math.Vector2, screen: pygame.Surface) -> None:
        image: pygame.Surface = pygame.image.load(
            f"assets/img/plants/{self.name}/farm_0.png"
        )
        super().__init__(image, pos, screen)
        pygame.time.set_timer(self.GROW_EVENT, 100)

    def grow(self) -> None:
        ...

    def rot(self) -> None:
        ...