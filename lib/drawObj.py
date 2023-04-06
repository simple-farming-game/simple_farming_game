import pygame

def drawObj(runtime_values, draw):
    # colors
    SKYBLUE = pygame.Color(113, 199, 245)
    BLACK = pygame.Color(0, 0, 0)
    WHITE = pygame.Color(255, 255, 255)

    # 버전변수
    version = runtime_values.version
    version_text = f"{version[0]} {version[1]}.{version[2]}.{version[3]}"

    # 폰트
    font_renderer = pygame.font.Font("assets/font/Galmuri.ttf", 20) \
    # 그리기
    runtime_values.screen.fill(SKYBLUE)  # 화면 채우기
    draw.draw_ground(runtime_values.screen)
    # 그외
    draw.draw_plants() # 식물
    draw.draw_players() # 플래이어
    # 글시
    draw.draw_text_with_border( # 버전명
        runtime_values.screen, font_renderer,
        f"SFG {version_text}!  {runtime_values.lang['guid']}",
        WHITE, BLACK, 2, pygame.math.Vector2(10, 10))

    draw.draw_text_with_border( # 좌표
        runtime_values.screen, font_renderer,
        str(runtime_values.players[0].get_tile_pos()),
        WHITE, BLACK, 2, pygame.math.Vector2(850, 35))

    draw.draw_text_with_border( # 셀렉트 아이템
        runtime_values.screen, font_renderer,
        f"{runtime_values.lang['select']} : {runtime_values.lang['items'][runtime_values.players[0].handle_item.name]}",
        WHITE, BLACK, 2, pygame.math.Vector2(10, 35))

    if runtime_values.players[0].handle_item in plants_list.plants_list: # type: ignore
        draw.draw_text_with_border( # 아이템 겟수
            runtime_values.screen, font_renderer,
            f"{runtime_values.lang['count']} : {str(runtime_values.players[0].inventory[runtime_values.players[0].handle_item.name])} {runtime_values.lang['seed']} : {runtime_values.players[0].inventory[f'{runtime_values.players[0].handle_item.name}_seed']}",
            WHITE, BLACK, 2, pygame.math.Vector2(10, 60))
        
    if runtime_values.players[0].handle_item.name == "VITAMIN":
        draw.draw_text_with_border( # 비타민 겟수
            runtime_values.screen, font_renderer,
            f"{runtime_values.lang['count']} : {runtime_values.players[0].inventory[runtime_values.players[0].handle_item.name]}",
            WHITE, BLACK, 2, pygame.math.Vector2(10, 60))
        
    draw.draw_text_with_border( # 좌표
        runtime_values.screen, font_renderer,
        f"{runtime_values.lang['gold']} : {runtime_values.players[0].inventory['gold']}",
        WHITE, BLACK, 2, pygame.math.Vector2(10, 85))