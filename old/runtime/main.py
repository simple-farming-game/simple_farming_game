import pygame;pygame.init()

var = "build 20221008a"

print(f"SFG {var}")

screen = pygame.display.set_mode((800, 500)) #화면 크기 설정
clock = pygame.time.Clock() 

#플래이어
playerImg = pygame.image.load("asset/img/player.png")
playerPos = [10,10]
dir = ""

#변수
gameStart = True
lsFont = pygame.font.Font( "asset/font/Galmuri.ttf", 20)
BLACK = ( 0, 0, 0 )
WHITE = (255, 255, 255)

tileMap=[
    [0,0,0,0,0],
    [0,1,2,0,0],
    [0,0,0,0,0],
    [0,0,0,0,0],
    [0,0,0,0,0]
];dirtImg = pygame.image.load("asset/img/dirt.png")

verText = lsFont.render(f"SFG {var}", True, BLACK)
verTextOutline = lsFont.render(f"SFG {var}", True, WHITE)


pygame.display.set_caption(f"SFG {var}")
while gameStart: #게임 루프
    screen.fill((122, 215, 255)) #단색으로 채워 화면 지우기

    #변수 업데이트


    #동시누를시 안움직여지게, 대각선 가능하게 수정예정(배경이 움직여지게)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameStart = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                dir = "u"
            if event.key == pygame.K_DOWN:
                dir = "d"
            if event.key == pygame.K_LEFT:
                dir = "l"
            if event.key == pygame.K_RIGHT:
                dir = "r"
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                dir = ""
            if event.key == pygame.K_DOWN:
                dir = ""
            if event.key == pygame.K_LEFT:
                dir = ""
            if event.key == pygame.K_RIGHT:
                dir = ""

    if dir == "u":
        playerPos[1]-=1
    elif dir == "d":
        playerPos[1]+=1
    elif dir == "l":
        playerPos[0]-=1
    elif dir == "r":
        playerPos[0]+=1

    #타일맵 출력
    """ for line in tileMap:
        tilePos = [32, 32]
        print(tilePos, line)
        for tile in line:
            print(tilePos, line, tile)
            if tile == 1:
                screen.blit(dirtImg, tilePos)
            tilePos[0] += 32
            print(tilePos, line, tile)
        tilePos[1] += 32
        print(tilePos, line) """
    

    #화면 그리기
    screen.blit(playerImg, (playerPos[0],playerPos[1]))
    screen.blit(verTextOutline, (10+2,10))
    screen.blit(verTextOutline, (10-2,10))
    screen.blit(verTextOutline, (10,10+2))
    screen.blit(verTextOutline, (10,10-2))
    screen.blit(verText, (10,10))  

    pygame.display.update() #모든 화면 그리기 업데이트
    clock.tick(170) #30 FPS (초당 프레임 수) 를 위한 딜레이 추가, 딜레이 시간이 아닌 목표로 하는 FPS 값

pygame.quit()    