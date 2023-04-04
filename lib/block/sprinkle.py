import pygame
import random

from . import Block


class Sprinkle(Block.Block):
    vitamin: bool = False
    name:str = "sprinkle"