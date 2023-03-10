import pygame


if __name__ == "__main__":
    from lib import player
    from lib import runtime_values
    runtime_values.players = [player.player(pygame.image.load(
        "assets/img/player.png"), pygame.math.Vector2(900, 100), runtime_values.screen, runtime_values.window_size)]
    from lib import draw
    from lib import keyinput
    from lib import farm

    runtime_values.running = True
    runtime_values.my_dir = player.Direction.STOP
    version = runtime_values.version
    version_text = f"{version[0]} {version[1]}.{version[2]}.{version[3]}"
    print(f'''
                        _    ___       ___
    _ __   _____      _| | _|_ _|_ __ |_ _|
    | '_ \\ / _ \\ \\ /\\ / / |/ /| || '_ \\ | |
    | | | |  __/\\ V  V /|   < | || | | || |
    |_| |_|\\___| \\_/\\_/ |_|\\_\\___|_| |_|___| Games
    ____         _____         ____
    / ___|       |  ___|       / ___|
    \\___ \\       | |_         | |  _
    ___) |      |  _|        | |_| |
    |____/ imple |_|  arming  \\____|ame
    
    V. {version_text}
    최고의 게발섭! mng커뮤니티! https://discord.gg/mng
    ''', end="")
    runtime_values.logs.info("Start Loading")

    # colors
    SKYBLUE = pygame.Color(113, 199, 245)
    BLACK = pygame.Color(0, 0, 0)
    WHITE = pygame.Color(255, 255, 255)

    font_renderer = pygame.font.Font("assets/font/Galmuri.ttf", 20)

    pygame.display.set_caption(
        f"sfg {version_text}! - by newkini")
    pygame.display.set_icon(pygame.image.load('assets/img/icon.png'))

    # 게임와일
    runtime_values.logs.info("Finish Loading")
    while runtime_values.running:
        runtime_values.clock.tick(100)
        runtime_values.screen.fill(SKYBLUE)  # 화면 채우기

        draw.draw_ground(runtime_values.screen)

        draw.draw_text_with_border(
            runtime_values.screen, font_renderer, f"SFG {version_text}!  {runtime_values.lang['guid']}", WHITE, BLACK, 2, pygame.math.Vector2(10, 10))
        draw.draw_text_with_border(
            runtime_values.screen, font_renderer, str(runtime_values.players[0].get_tile_pos()), WHITE, BLACK, 2, pygame.math.Vector2(850, 35))
        draw.draw_text_with_border(
            runtime_values.screen, font_renderer, "inventory : "+str(runtime_values.players[0].inventory), WHITE, BLACK, 2, pygame.math.Vector2(10, 35))
        draw.draw_text_with_border(
            runtime_values.screen, font_renderer, "select : "+runtime_values.lang["items"][runtime_values.players[0].handle_item.name], WHITE, BLACK, 2, pygame.math.Vector2(10, 70))
        draw.draw_plants()
        draw.draw_players()
        keyinput.process()
        runtime_values.players[0].move(runtime_values.my_dir)

        farm.grow_plants()

        pygame.display.update()  # 화면 업데이트

    runtime_values.logs.info("quit")
    runtime_values.logs.save()
    pygame.quit()
