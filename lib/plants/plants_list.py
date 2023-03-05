from typing import Union,  get_args

from . import rice
from . import test_potato

plants_type = Union[
    rice.rice,
    test_potato.potato
]
plants_list = get_args(plants_type)
