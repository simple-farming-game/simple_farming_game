import pygame
import platform
import json
import os
from typing import Tuple

from lib.logger import logger
from lib import player

version_type = Tuple[str, int, int, int]
version: version_type = ("devalpha", 2, 1, 0)

comInfo = {
    "core": os.cpu_count(),
    "os": platform.system(),
    "processor": platform.processor(),
    "osvar": platform.version()
}

setting = {}
lang = {}


window_size = (960, 640)
screen = pygame.display.set_mode(window_size)
clock = pygame.time.Clock()

logs = logger()

running: bool

players: list[player.player]
my_dir: player.Direction
fps: int = 100