from typing import Union, get_args, cast

from . import box
from . import sprinkle

block_type = Union[
    box.Box,
    sprinkle.Sprinkle
]
block_list = cast(tuple[block_type], get_args(block_type))

def next_block(block: block_type) -> block_type:
    now_index: int
    for index, item in enumerate(block_list):
        if item == block:
            now_index = index

    if len(block_list) == now_index:  # type: ignore
        return block_list[0]
    else:
        return block_list[now_index + 1]  # type:ignore