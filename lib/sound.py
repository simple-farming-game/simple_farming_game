import pygame
import os

file_list = os.listdir("assets/sound")
sounds: dict[str,pygame.mixer.Sound] = {}

for file in file_list:
    if file.find(".ogg") != -1:
        sounds[file.replace(".ogg","")] = pygame.mixer.Sound(f"assets/sound/{file}")

sounds["farm"].play()
