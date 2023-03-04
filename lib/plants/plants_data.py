from typing import NewType, Union
import pygame

from ..Object import Object

from . import rice
from . import test_potato


class Plants(Object):
    name: str  # 영어로 적고 lang 파일에서 참조.

    def __init__(self, image: pygame.Surface, pos: pygame.math.Vector2, screen: pygame.Surface) -> None:
        super().__init__(image, pos, screen)

    def grow(self) -> None: ...


# class Plants_type(Enum):
#     """
#     마음엔 안들지만, 전보단 낫네요 ㅋㅋ
#     """
#     rice.rice = auto()
plants_list = [
    rice.rice,
    test_potato.potato
]
Plants_type = NewType("Plants_type", Union[*plants_list])  # 외앉되;;
