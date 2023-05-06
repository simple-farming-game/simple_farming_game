from typing import Union, get_args, cast
import pygame

from . import box
from . import sprinkle

block_type = Union[
    box.Box,
    sprinkle.Sprinkle
]
block_list = cast(tuple[block_type], get_args(block_type))
block_image = [pygame.transform.scale(pygame.image.load(f"assets/img/block/{i.name}.png"),(32,32)) for i in block_list]
block_name = [i.name for i in block_list]
def next_block(block: block_type) -> block_type:
    now_index: int
    for index, item in enumerate(block_list):
        if item == block:
            now_index = index

    if len(block_list) == now_index:  # type: ignore
        return block_list[0]
    else:
        return block_list[now_index + 1]  # type:ignore