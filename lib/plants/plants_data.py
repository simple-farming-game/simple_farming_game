from dataclasses import dataclass
from enum import Enum, auto
import pygame

from ..Object import Object
from ..types.Image import Image

from . import rice


@dataclass
class Plants_data:
    img: Image


class Plants(Object):
    name: str  # 영어로 적고 lang 파일에서 참조.
    plants_data: Plants_data

    def __init__(self, image: Image, pos: pygame.math.Vector2, screen: pygame.Surface, plants_data: Plants_data) -> None:
        super().__init__(image, pos, screen)
        self.plants_data = plants_data

    def grow(self) -> None: ...


class Plants_type(Enum):
    """
    마음엔 안들지만, 전보단 낫네요 ㅋㅋ
    """
    rice.rice = auto()
