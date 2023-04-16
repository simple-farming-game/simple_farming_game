import pygame
import platform
import json
import os
from typing import Tuple

from lib.logger import logger
from lib import player

version_type = Tuple[str, int, int, int]
version: version_type = ("alpha", 2, 1, 9)

pcInfo = {
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

players: list[player.player] = []
my_dir: player.Direction = player.Direction.STOP
fps: int = 100

on_setting = False
font = pygame.font.Font("assets/font/Galmuri.ttf", 20)

SKYBLUE = pygame.Color(113, 199, 245)
BLACK = pygame.Color(0, 0, 0)
WHITE = pygame.Color(255, 255, 255)