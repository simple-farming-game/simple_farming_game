import pygame
import tkinter

from . import Block

class Shop(Block.Block):
    is_shop_opne: bool = False
    name: str = "shop"
    
    def init(self):
        pass
    
    def interact(self):
        root = tkinter.Tk()
 
        nameLabel = tkinter.Label(root, text=f"")
        nameLabel.grid(row=0, column=0)
        countLabel = tkinter.Button(root, text=f"")
        countLabel.grid(row=1, column=0)

        root.mainloop()
        
    @staticmethod
    def draw_text_with_border(screen: pygame.Surface, font: pygame.font.Font, text: str, inside_color: pygame.Color, border_color: pygame.Color, border_size: float, positon: pygame.math.Vector2):
        inside = font.render(text, True, inside_color)
        border = font.render(text, True, border_color)

        screen.blit(border, pygame.math.Vector2(positon.x-border_size, positon.y))
        screen.blit(border, pygame.math.Vector2(positon.x+border_size, positon.y))
        screen.blit(border, pygame.math.Vector2(positon.x, positon.y-border_size))
        screen.blit(border, pygame.math.Vector2(positon.x, positon.y+border_size))
        screen.blit(inside, positon)