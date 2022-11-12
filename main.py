import sys
import os
import pygame
import pytmx
import math
import asset.tilemap.farm as farm

pygame.init()

# 함수

# 변수
var = "alpha"
hw = (960, 640)
running = True
screen = pygame.display.set_mode(hw)
clock = pygame.time.Clock() 
# 색변수
SKYBLUE = (113, 199, 245)
BLACK = (255,255,255)
WHITE = (0,0,0)
# 플래이어 변수
playerImg = pygame.image.load("asset/img/player.png")
playerPos = [100,100]
plyerTilePos = [math.trunc(playerPos[0]/32),math.trunc(playerPos[1]/32)]
# 타일맵
tmxFile = pytmx.load_pygame('asset/tilemap/farm.tmx')
dirtImg = pygame.image.load("asset/img/dirt.png")
farmlandImg = pygame.image.load("asset/img/farmland.png")

# 글시
lsFont = pygame.font.Font( "asset/font/Galmuri.ttf", 20)

verText = lsFont.render(f"SFG {var}!  플래이어 왼쪽위가 기준입니다!", True, BLACK)
verTextOutline = lsFont.render(f"SFG {var}!  플래이어 왼쪽위가 기준입니다!", True, WHITE)

# 세팅
pygame.display.set_caption(f"sfg {var}! - by newkin")

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
            if event.key == pygame.K_f:
                farm.tileMap[plyerTilePos[0]][plyerTilePos[1]] = 2
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
    # 중심잡기
    
    # 타일맵 https://codememo.tistory.com/21
    tilePos = [0,0]
    for line in farm.tileMap:
        for tile in line:
            if tile == 1:
                screen.blit(dirtImg, tilePos)
            if tile == 2:
                screen.blit(farmlandImg, tilePos)
            tilePos[0] += 32
        tilePos[1] += 32
        tilePos[0] = 0

    # 밭 갈기
    
    
    # 이미지 그리기
    screen.blit(playerImg, playerPos)
    screen.blit(verTextOutline, (10+2,10))
    screen.blit(verTextOutline, (10-2,10))
    screen.blit(verTextOutline, (10,10+2))
    screen.blit(verTextOutline, (10,10-2))
    screen.blit(verText, (10,10)) 

    pygame.display.update() # 화면 업데이트

pygame.quit()