from typing import Union, get_args, cast
import pygame

from . import rice
from . import tomato
from . import sunFlower
from . import carrots

plants_type = Union[rice.Rice, tomato.Tomato, sunFlower.SunFlower, carrots.Carrots]
plants_list = cast(tuple[plants_type], get_args(plants_type))
plants_name: list[str] = [i.name for i in plants_list]
plants_image: list[pygame.Surface] = [
    pygame.transform.scale(
        pygame.image.load(f"assets/img/plants/{i.name}/item.png"), (32, 32)
    )
    for i in plants_list
]
plants_seed_name: list[str] = [f"{i.name}_seed" for i in plants_list]
plants_seed_image: list[pygame.Surface] = [
    pygame.transform.scale(
        pygame.image.load(f"assets/img/plants/{i.name}/seed.png"), (32, 32)
    )
    for i in plants_list
]


def next_plant(plant: plants_type) -> plants_type:
    now_index: int
    for index, item in enumerate(plants_list):
        if item == plant:
            now_index = index

    if len(plants_list) == now_index:  # type: ignore
        return plants_list[0]
    else:
        return plants_list[now_index + 1]  # type:ignore
