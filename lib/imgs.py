import pygame
from lib.plants import plants_list

imgs: dict[str, pygame.Surface] = {
    "mus": pygame.image.load("assets/img/mouse_cus.png"),
    "item_bar": pygame.transform.scale(
        pygame.image.load("assets/img/ui/item_bar.png"), (256, 32)
    ),
    "item_bar_select": pygame.image.load("assets/img/ui/select_item_bar.png"),
}
emojis: dict[str, pygame.Surface] = {
    "smile": pygame.image.load("assets/img/emoji/smile.png"),
    "angry": pygame.image.load("assets/img/emoji/angry.png"),
}


def img(imgName):
    return imgs[imgName]  # type: ignore
