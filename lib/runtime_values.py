import pygame
import datetime
from typing import Tuple, List

from lib import player

version_type = Tuple[str, int, int, int]
version: version_type = ("alpha", 2, 1, 5)

setting: dict
lang: dict
start_time: datetime.datetime

window_size = (960, 640)
screen = pygame.display.set_mode(window_size)
clock = pygame.time.Clock()

running: bool

players: list[player.Player]
my_dir: player.Direction
fps: int = 100

logs: List[str]
