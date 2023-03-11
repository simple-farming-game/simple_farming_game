from typing import Union, get_args, cast

from . import rice
from . import tomato
from . import sunFlower

plants_type = Union[
    rice.rice,
    tomato.Tomato,
    sunFlower.SunFlower
]
plants_list = cast(tuple[plants_type], get_args(plants_type))


def next_plant(plant: plants_type) -> plants_type:
    now_index: int
    for index, item in enumerate(plants_list):
        if item == plant:
            now_index = index

    if len(plants_list) == now_index:  # type: ignore
        return plants_list[0]
    else:
        return plants_list[now_index + 1]  # type:ignore
