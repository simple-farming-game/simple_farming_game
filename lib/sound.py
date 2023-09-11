import pygame
import os
import ffmpeg

input_folder = 'assets/sound'  # 입력 폴더 경로
output_folder = 'assets/sound'  # 출력 폴더 경로

for root, dirs, files in os.walk(input_folder):
    for file in files:
        if file.endswith(".mp3"):
            input_file = os.path.join(root, file)
            output_file = os.path.join(output_folder, os.path.splitext(file)[0] + ".ogg")
            
            stream = ffmpeg.input(input_file)
            stream = ffmpeg.output(stream, output_file, ab='192k', loglevel="quiet")
            ffmpeg.run(stream)
        elif file.endswith(".ogg"):
            pass


pygame.init()

file_list = os.listdir("assets/sound")
sounds: dict[str,pygame.mixer.Sound] = {}

for file in file_list:
    if file.find(".ogg") != -1:
        sounds[file.replace(".ogg","")] = pygame.mixer.Sound(f"assets/sound/{file}")

sounds["farm"].play()
