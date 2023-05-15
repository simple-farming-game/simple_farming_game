import pygame


from . import Block
from . import block_list
from ..plants import plants_list
from .. import shopGui

class Shop(Block.Block):
    is_shop_opne: bool = False
    name: str = "shop"
    
    def init(self):
        pass
    
    def interact(self):
        shopGui.shop_opne(block_list, plants_list)
        
    @staticmethod
    def draw_text_with_border(screen: pygame.Surface, font: pygame.font.Font, text: str, inside_color: pygame.Color, border_color: pygame.Color, border_size: float, positon: pygame.math.Vector2):
        inside = font.render(text, True, inside_color)
        border = font.render(text, True, border_color)

        screen.blit(border, pygame.math.Vector2(positon.x-border_size, positon.y))
        screen.blit(border, pygame.math.Vector2(positon.x+border_size, positon.y))
        screen.blit(border, pygame.math.Vector2(positon.x, positon.y-border_size))
        screen.blit(border, pygame.math.Vector2(positon.x, positon.y+border_size))
        screen.blit(inside, positon)