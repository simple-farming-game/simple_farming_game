import sys
import pygame
from lib.runtime_values import *
from lib import farm
from lib import save

pygame.init()
logger.info("파이게임 초기화.")

ground_images: dict[farm.Tiles, pygame.Surface] = {
    farm.Tiles.DIRT: pygame.image.load("assets/img/ground/dirt.png"),
    farm.Tiles.FARMLAND: pygame.image.load("assets/img/ground/farmland.png"),
    farm.Tiles.WATER_FARMLAND: pygame.image.load("assets/img/ground/water_farmland.png"),
}

save.import_save()

while is_running:
    dt: float = clock.tick(100) / 1000
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
    
    screen.fill(SKYBLUE)
    
    tilePos = pygame.math.Vector2(0, 0)
    for line in farm.tileMap:
        for tile in line:
            screen.blit(ground_images[farm.Tiles.DIRT], tilePos)
            screen.blit(ground_images[tile], tilePos)
            tilePos.y += 32
        tilePos.x += 32
        tilePos.y = 0
    
    pygame.display.update()

logger.info("로그, 세이브저장, 종료를 시작합니다.")
save.write_save()
logger.save()
logger.info("저장성공!")
pygame.quit()
sys.exit()