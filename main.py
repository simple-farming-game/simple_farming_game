import sys
import os
import pygame
import pytmx

pygame.init()

# 변수
running = True
screen = pygame.display.set_mode((960, 640))
clock = pygame.time.Clock() 
# 색변수
SKYBLUE = (113, 199, 245)
# 플래이어 변수
playerImg = pygame.image.load("asset/img/player.png")
playerPos = [100,100]
# 타일맵
tmxFile = pytmx.load_pygame('asset/tilemap/farm.tmx')

# 세팅
pygame.display.set_caption("sfg alpha! - by newkin")

# 게임와일
while running:
    screen.fill(SKYBLUE) # 화면 채우기
    
    for event in pygame.event.get():  # 키입력 감지
        # 나가기
        if event.type == pygame.QUIT:  # 나가기 버튼 눌럿을때
            running = False  # 와일문 나가기
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                dir = "l"
            elif event.key == pygame.K_d:
                dir = "r"
            elif event.key == pygame.K_w:
                dir = "u"
            elif event.key == pygame.K_s:
                dir = "d"
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                dir = ""
            elif event.key == pygame.K_d:
                dir = ""
            elif event.key == pygame.K_w:
                dir = ""
            elif event.key == pygame.K_s:
                dir = ""
            
    # 플래이어
    # 움직이기
    speed = 1
    if dir == "l":
        playerPos[0] -= speed
    elif dir == "r":
        playerPos[0] += speed
    elif dir == "u":
        playerPos[1] -= speed
    elif dir == "d":
        playerPos[1] += speed

    # 타일맵 https://codememo.tistory.com/21
    for layer in tmxFile.visible_layers:
        for x, y, gid, in layer:
            tile = tmxFile.get_tile_image_by_gid(gid)
            if tile:
                screen.blit(tile, (x * tmxFile.tilewidth, y * tmxFile.tileheight))
    
    # 이미지 그리기
    screen.blit(playerImg, playerPos)

    pygame.display.update() # 화면 업데이트

pygame.quit()