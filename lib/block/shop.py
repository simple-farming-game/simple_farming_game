import pygame

from . import Block

class Shop(Block.Block):
    is_shop_opne: bool = False
    name: str = "shop"
    
    def init(self):
        pass
    
    def interact(self):
        self.is_shop_opne = not self.is_shop_opne
        
    @staticmethod
    def draw_text_with_border(screen: pygame.Surface, font: pygame.font.Font, text: str, inside_color: pygame.Color, border_color: pygame.Color, border_size: float, positon: pygame.math.Vector2):
        inside = font.render(text, True, inside_color)
        border = font.render(text, True, border_color)

        screen.blit(border, pygame.math.Vector2(positon.x-border_size, positon.y))
        screen.blit(border, pygame.math.Vector2(positon.x+border_size, positon.y))
        screen.blit(border, pygame.math.Vector2(positon.x, positon.y-border_size))
        screen.blit(border, pygame.math.Vector2(positon.x, positon.y+border_size))
        screen.blit(inside, positon)

    def update(self):
        from .. import runtime_values
        if self.is_shop_opne:
            self.draw_text_with_border(
                runtime_values.screen, runtime_values.font,
                "상점",
                runtime_values.WHITE, runtime_values.BLACK, 2, pygame.math.Vector2(15*32, 5*32))