import pygame

imgs: dict[str, pygame.Surface] = {
    "mus" : pygame.image.load("assets/img/mouse_cus.png")
}

def img(imgName):
    return imgs[imgName] # type: ignore