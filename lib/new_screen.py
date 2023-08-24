import pygame
from lib import runtime_values
from enum import Enum

class color(Enum):
    SKYBLUE = pygame.Color(113, 199, 245)
    BLACK = pygame.Color(0, 0, 0)
    WHITE = pygame.Color(255, 255, 255)
    BLUE = pygame.Color(61, 139, 255)

def background(color: Enum):
    # pygame.draw.rect(runtime_values.screen, color.value, pygame.Rect(0,0,runtime_values.window_size[0],runtime_values.window_size[1]))
    runtime_values.screen.fill(color.value)