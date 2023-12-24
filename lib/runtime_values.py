import pygame
from lib.log4py import Logger

# Var
screen_size: tuple = (960, 640)
is_running: bool = True
logger = Logger()

# Color
SKYBLUE = pygame.Color(113, 199, 245)

# Pygame Var
screen: pygame.Surface = pygame.display.set_mode(screen_size)
clock: pygame.time.Clock = pygame.time.Clock()