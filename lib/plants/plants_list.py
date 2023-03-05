from typing import Union, get_args, cast

from . import rice
from . import test_potato

plants_type = Union[
    rice.rice,
    test_potato.potato
]
plants_list = cast(tuple[plants_type], get_args(plants_type))
