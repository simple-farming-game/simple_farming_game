import pygame

pygame.init()

# 변수
running = True
screen = pygame.display.set_mode((400, 700))
clock = pygame.time.Clock() 
# 색변수
SKYBLUE = (113, 199, 245)

# 게임와일
while running:
    screen.fill(SKYBLUE) # 화면 채우기
    
    for event in pygame.event.get():  # 키입력 감지
        # 나가기
        if event.type == pygame.QUIT:  # 나가기 버튼 눌럿을때
            running = False  # 와일문 나가기
    
    pygame.display.update() # 화면 업데이트

pygame.surface
pygame.quit() # 게임 나가기