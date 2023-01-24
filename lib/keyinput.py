import lib.rice as rice
import lib.farm as farm
import json
import random
import pygame
dir = ""

def key(selectImg, riceClass, farmRiceImg, screen, playerTilePos, stop, delrice, riceSerci, playerClass, reload):
    global dir

    def key_d():
        if (selectImg[1] == 1) and (farm.tileMap[playerTilePos[1]][playerTilePos[0]] == 2) and (playerClass.inventory["riceSeed"] > 0):  # 심기
            farm.tileMap[playerTilePos[1]][playerTilePos[0]] = 3
            riceClass.append(
                rice.rice(farmRiceImg, screen, playerTilePos))
            playerClass.inventory["riceSeed"] -= 1
            print(f"심기 : X:{playerTilePos[1]} Y:{playerTilePos[0]}")

        elif (selectImg[1] == 2) and (farm.tileMap[playerTilePos[1]][playerTilePos[0]] == 1):  # 경작
            farm.tileMap[playerTilePos[1]][playerTilePos[0]] = 2
            print(f"경작 : X:{playerTilePos[1]} Y:{playerTilePos[0]}")

        elif (selectImg[1] == 4) and (farm.tileMap[playerTilePos[1]][playerTilePos[0]] == 3) and (riceSerci(playerTilePos[1], playerTilePos[0]).age == 2):  # 캐기
            farm.tileMap[playerTilePos[1]][playerTilePos[0]] = 2
            delrice(playerTilePos[1], playerTilePos[0])
            playerClass.inventory["riceSeed"] += random.randint(0, 4)
            playerClass.inventory["rice"] += random.randint(0, 4)

        elif (selectImg[1] == 3) and ((farm.tileMap[playerTilePos[1]][playerTilePos[0]] == 2)): # 삽 
            farm.tileMap[playerTilePos[1]][playerTilePos[0]] = 1

        else:
            print("실패 : 이미 심어져 있거나, 심을 수 있는 타입이 아님")

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            stop()  # 와일문 나가기
        if event.type == pygame.KEYDOWN:
            match event.key:
                case pygame.K_LEFT: dir = "l"
                case pygame.K_RIGHT: dir = "r"
                case pygame.K_UP: dir = "u"
                case pygame.K_DOWN: dir = "d"
                case pygame.K_d: key_d()
                case pygame.K_z:  # 선택 해제
                    selectImg[0] = pygame.image.load("assets/img/none.png")
                    selectImg[1] = 0
                case pygame.K_r:  # 씨앗 선택
                    selectImg[0] = pygame.image.load("assets/img/rice_seed.png")
                    selectImg[1] = 1
                case pygame.K_f:  # 낫 선택
                    selectImg[0] = pygame.image.load("assets/img/hoe.png")
                    selectImg[1] = 2
                case pygame.K_s:  # 삽 선택
                    selectImg[0] = pygame.image.load("assets/img/shovel.png")
                    selectImg[1] = 3
                case pygame.K_e:  # 괭이 선택
                    selectImg[0] = pygame.image.load("assets/img/sickle.png")
                    selectImg[1] = 4
                case pygame.K_SPACE:  # 괭이 선택
                    playerClass.speed=2.5
                case pygame.K_t:
                    save = open("save.sfgsave","w")
                    save.write(json.dumps({"tile":farm.tileMap,"inv":playerClass.inventory,"pos":playerClass.pos}))
                    save.close()
                    print("저장")
                case pygame.K_y:
                    try:
                        save = open("save.sfgsave","r")
                        saveData = json.load(save)
                        playerClass.inventory=saveData["inv"]
                        farm.tileMap=saveData["tile"]
                        playerClass.pos=saveData["pos"]
                        reload()
                        pos = [0, 0]
                        tilePos=[0,0]
                        for line in farm.tileMap:
                            for tile in line: 
                                if tile == 3:
                                    riceClass.append(rice.rice(farmRiceImg, screen, tilePos))
                                pos[0] += 32
                                tilePos[0] += 1
                            pos[1] += 32
                            tilePos[1] += 1
                            pos[0] = 0
                            tilePos[0]=0
                        save.close()
                        print("불러오기")
                    except:
                        print("저장파일이 없음")

        if event.type == pygame.KEYUP:
            match event.key:
                case pygame.K_UP | pygame.K_DOWN | pygame.K_LEFT | pygame.K_RIGHT:
                    dir = ""
                case pygame.K_SPACE:
                    playerClass.speed = 1
