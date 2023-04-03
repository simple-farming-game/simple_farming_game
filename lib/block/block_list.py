from typing import Union, get_args, cast

from . import box
from . import sprinkle

block_type = Union[
    box.Box,
    sprinkle.Sprinkle
]
