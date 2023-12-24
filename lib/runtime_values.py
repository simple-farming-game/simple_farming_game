import pygame
from lib.log4py import Logger

# Var
screen_size: tuple = (960, 640)
is_running: bool = True
logger: Logger = Logger()
version: tuple[int, int, int, str] = (0, 2, 0, "alpha")
ver_text = f"{version[0]}.{version[1]}.{version[2]} {version[3]}"

# Color
SKYBLUE:pygame.Color = pygame.Color(113, 199, 245)

# Pygame Var
screen: pygame.Surface = pygame.display.set_mode(screen_size)
clock: pygame.time.Clock = pygame.time.Clock()