import pygame
import platform
import json
import os
from typing import Tuple

from lib.logger import logger
from lib import player

version_type = Tuple[str, int, int, int]
version: version_type = ("alpha", 2, 0, 2)

comInfo = {
    "core": os.cpu_count(),
    "os": platform.system(),
    "processor": platform.processor(),
    "osvar": platform.version()
}

with open("data/setting.json", 'r', encoding='utf8') as setting_file:
    setting = json.load(setting_file)
with open(f"data/lang/{setting['lang']}.json", 'r', encoding='utf8') as lang_file:
    lang = json.load(lang_file)


pygame.init()
window_size = (960, 640)
screen = pygame.display.set_mode(window_size)
clock = pygame.time.Clock()

logs = logger()

running: bool

players: list[player.player]
my_dir: player.Direction
