import file.code.rice as rice
import file.code.farm as farm
import pygame
dir = ""
def key(selectImg,riceClass,farmRiceImg,screen,playerTilePos,stop,delrice,riceSerci):
    global dir
    for event in pygame.event.get():  # 키입력 감지
        # 나가기
        if event.type == pygame.QUIT:  # 나가기 버튼 눌럿을때
            stop()  # 와일문 나가기
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
                    farm.tileMap[playerTilePos[1]][playerTilePos[0]] = 3
                    riceClass.append(rice.rice(farmRiceImg,screen,playerTilePos))
                    print(f"심기 : X:{playerTilePos[1]} Y:{playerTilePos[0]}")
                elif (selectImg[1] == 2) and (farm.tileMap[playerTilePos[1]][playerTilePos[0]] == 1):
                    farm.tileMap[playerTilePos[1]][playerTilePos[0]] = 2
                    print(f"경작 : X:{playerTilePos[1]} Y:{playerTilePos[0]}")
                elif (selectImg[1] == 4) and (farm.tileMap[playerTilePos[1]][playerTilePos[0]] == 3) and (riceSerci(playerTilePos[1],playerTilePos[0]).age==3):
                    farm.tileMap[playerTilePos[1]][playerTilePos[0]] = 2
                    delrice(playerTilePos[1],playerTilePos[0])
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
            elif event.key == pygame.K_e: # 수확
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