from typing import Union, get_args, cast
import pygame

from . import sprinkle
from . import shop

block_type = Union[sprinkle.Sprinkle, shop.Shop]
block_list = cast(tuple[block_type], get_args(block_type))
block_name: list[str] = [i.name for i in block_list]
block_image: list[pygame.Surface] = [
    pygame.transform.scale(
        pygame.image.load(f"assets/img/block/{i.name}.png"), (32, 32)
    )
    for i in block_list
]


def next_block(block: block_type) -> block_type:
    now_index: int
    for index, item in enumerate(block_list):
        if item == block:
            now_index = index

    if len(block_list) == now_index:  # type: ignore
        return block_list[0]
    else:
        return block_list[now_index + 1]  # type:ignore
