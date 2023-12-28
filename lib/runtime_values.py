import pygame
from lib.log4py import Logger
from lib import player
from lib.player import Direction

# Var
screen_size: tuple = (960, 640)
is_running: bool = True
logger: Logger = Logger()
version: tuple[int, int, int, str] = (0, 3, 0, "alpha")
ver_text = f"{version[0]}.{version[1]}.{version[2]} {version[3]}"
# player var
player_img: pygame.Surface = pygame.image.load("assets/img/player.png")
playerc = player.Player(player_img, pygame.Vector2(0,0), 3)
player_dir: Direction = Direction.STOP

# Color
SKYBLUE:pygame.Color = pygame.Color(113, 199, 245)

# Pygame Var
screen: pygame.Surface = pygame.display.set_mode(screen_size)
clock: pygame.time.Clock = pygame.time.Clock()