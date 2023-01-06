'''
newkini! - sfg
만들꺼:
언어 변경
ide(?)
'''
import pygame
import file.asset.tilemap.farm as farm
import file.code.player as player
import file.code.rice as rice
import file.code.sfgchat as sfgchat

sfgchat.runchat()

print("TESTER : OTTO\nIF MACOS : SYSTEM SETING > KEYBORD > INPUT SOURCE > CAPS LOOK KEY ABC INPUT SOURCE TRANSFORM OFF")

pygame.init()

# 함수

# 변수
var = "alpha 1.1/6"
hw = (960, 640)
running = True
screen = pygame.display.set_mode(hw)
clock = pygame.time.Clock()
riceCon = 0
# 색변수
SKYBLUE = (113, 199, 245)
BLACK = (255,255,255)
WHITE = (0,0,0)
# 플래이어 변수
playerImg = pygame.image.load("file/asset/img/player.png")
playerPos = [900,100]
# 타일맵
dirtImg = pygame.image.load("file/asset/img/dirt.png")
farmlandImg = pygame.image.load("file/asset/img/farmland.png")
farmRiceImg = pygame.image.load("file/asset/img/farm_rice_0.png")
# 글시
lsFont = pygame.font.Font( "file/asset/font/Galmuri.ttf", 20)
# 이미지
selectImg = [pygame.image.load("file/asset/img/rice_seed.png"), 1]
# 좌표
selectPos = [0,50]



# 세팅
pygame.display.set_caption(f"sfg {var}! - by newkin")
playerClass = player.player(playerPos, screen, hw)
riceClass = []


# 게임와일
while running:
    clock.tick(100)

    playerTilePos = playerClass.playerTilePos
    verText = lsFont.render(f"SFG {var}!  플래이어 왼쪽위가 기준입니다!                                                {playerTilePos}", True, BLACK)
    verTextOutline = lsFont.render(f"SFG {var}!  플래이어 왼쪽위가 기준입니다!                                                {playerTilePos}", True, WHITE)

    screen.fill(SKYBLUE) # 화면 채우기
    
    for event in pygame.event.get():  # 키입력 감지
        # 나가기
        if event.type == pygame.QUIT:  # 나가기 버튼 눌럿을때
            running = False  # 와일문 나가기
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                dir = "l"
            elif event.key == pygame.K_RIGHT:
                dir = "r"
            elif event.key == pygame.K_UP:
                dir = "u"
            elif event.key == pygame.K_DOWN:
                dir = "d"
            if event.key == pygame.K_d:
                if (selectImg[1] == 1) and (farm.tileMap[playerTilePos[1]][playerTilePos[0]] == 2):
                    # farm.tileMap[playerTilePos[1]][playerTilePos[0]] = 3
                    riceClass.append(rice.rice(farmRiceImg,screen,playerTilePos))
                    print(f"심기 : X:{playerTilePos[1]} Y:{playerTilePos[0]}")
                elif (selectImg[1] == 2) and (farm.tileMap[playerTilePos[1]][playerTilePos[0]] == 1):
                    farm.tileMap[playerTilePos[1]][playerTilePos[0]] = 2
                    print(f"경작 : X:{playerTilePos[1]} Y:{playerTilePos[0]}")
                else:
                    print("실패 : 이미 심어져 있음.")
            if event.key == pygame.K_f:
                selectImg[0] = pygame.image.load("file/asset/img/farmland.png") # 괭이 이미지로 변경
                selectImg[1] = 2
            if event.key == pygame.K_z:
                selectImg[0] = pygame.image.load("file/asset/img/none.png")
                selectImg[1] = 0
            elif event.key == pygame.K_r:
                selectImg[0] = pygame.image.load("file/asset/img/rice_seed.png")
                selectImg[1] = 1
            elif event.key == pygame.K_s: # 지우기 심어진 상태 > 안심어진상태 > 흙
                selectImg[0] = pygame.image.load("file/asset/img/shovel.png")
                selectImg[1] = 3
            elif event.key == pygame.K_e: # 캐기
                selectImg[0] = pygame.image.load("file/asset/img/shovel.png") # 낫으로 변경
                selectImg[1] = 4
            # todo:뼛가루 추가, 뼛가루와 씨앗은 소모되게, 수확하면 씨앗 나오게 둘다 기본으로 5게,씨, 뼛가루 등은 인벤토리를 만들어서아이템을 클릭하면 선택되게(미래의 내가 잘 만들어 주겠지?) 만들다가 포기했네...
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                dir = ""
            elif event.key == pygame.K_DOWN:
                dir = ""
            elif event.key == pygame.K_LEFT:
                dir = ""
            elif event.key == pygame.K_RIGHT:
                dir = ""   
    # 플래이어
    # 경계
    # 움직이기
    playerClass.move()
    # 타일맵
    tilePos = [0,0]
    for line in farm.tileMap:
        for tile in line:
            if tile == 1:
                screen.blit(dirtImg, tilePos)
            if tile == 2:
                screen.blit(farmlandImg, tilePos)
            if tile == 3:
                screen.blit(farmRiceImg, tilePos)
            tilePos[0] += 32
        tilePos[1] += 32
        tilePos[0] = 0
    # 자라게


    # 드로우
    # riceClass.draw(farmRiceImg)
    for i in range(len(riceClass)):
        riceClass[i].draw()
        riceClass[i].grow()

    
    # 이미지 그리기
    playerClass.draw(playerImg)
    screen.blit(selectImg[0], selectPos)
    screen.blit(verTextOutline, (10+2,10))
    screen.blit(verTextOutline, (10-2,10))
    screen.blit(verTextOutline, (10,10+2))
    screen.blit(verTextOutline, (10,10-2))
    screen.blit(verText, (10,10))

    pygame.display.update() # 화면 업데이트
    playerClass.update(dir)
    # riceClass.update(playerClass.playerTilePos)

pygame.quit()