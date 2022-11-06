import pygame
import pytmx

pygame.init()

# 변수
running = True
screen = pygame.display.set_mode((500, 400))
clock = pygame.time.Clock() 
# 색변수
SKYBLUE = (113, 199, 245)
# 플래이어 변수
playerImg = pygame.image.load("asset/img/player.png")
playerPos = [100,100]
# 타일맵
tiled_map = pytmx.TiledMap.from_xml_string(some_string_here)

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
    speed = 0.1
    if dir == "l":
        playerPos[0] -= speed
    elif dir == "r":
        playerPos[0] += speed
    elif dir == "u":
        playerPos[1] -= speed
    elif dir == "d":
        playerPos[1] += speed
        
    # 이미지 그리기
    screen.blit(playerImg, playerPos)
    
    pygame.display.update() # 화면 업데이트

pygame.quit()