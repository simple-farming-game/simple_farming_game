import pygame
import json


if __name__ == "__main__":
    pygame.init()
    # runtime values
    from lib import player
    from lib import runtime_values
    from lib import imgs

    runtime_values.players = [player.player(pygame.image.load(
        "assets/img/player.png"), pygame.math.Vector2(900, 100), runtime_values.screen, runtime_values.window_size)]
    
    with open("data/setting.json", 'r', encoding='utf8') as setting_file: # open setting file
        runtime_values.setting = json.load(setting_file)
    with open(f"data/lang/{runtime_values.setting['lang']}.json", 'r', encoding='utf8') as lang_file: # open language file
        runtime_values.lang = json.load(lang_file)
        
    runtime_values.running = True
    runtime_values.my_dir = player.Direction.STOP

    # version variables
    version = runtime_values.version
    version_text = f"{version[0]} {version[1]}.{version[2]}.{version[3]}"

    from lib import draw
    from lib import keyinput
    from lib import farm

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
    최고의 개발섭! mng커뮤니티! https://discord.gg/mng
    ''', end="")
    runtime_values.logs.info("Start Loading")

    # Define variables
    # Define colors
    SKYBLUE = pygame.Color(113, 199, 245)
    BLACK = pygame.Color(0, 0, 0)
    WHITE = pygame.Color(255, 255, 255)

    # Define font
    font_renderer = pygame.font.Font("assets/font/Galmuri.ttf", 20)

    # Set game settings
    pygame.display.set_caption(f"sfg {version_text}! - by newkini") # Set window title
    pygame.display.set_icon(pygame.image.load('assets/img/icon.png')) # Set window icon
    pygame.mouse.set_visible(False) # Hide mouse cursor

    '''
    Game loop
    '''
    runtime_values.logs.info("Finish Loading")
    while runtime_values.running:
        musPos: tuple = pygame.mouse.get_pos() # Get mouse position
        df = runtime_values.clock.tick(runtime_values.fps) / 1000 # Get delta time
        runtime_values.clock.tick(runtime_values.fps)

        '''
        Drawing
        '''
        # Draw screen
        runtime_values.screen.fill(SKYBLUE)  # Fill screen
        draw.draw_ground(runtime_values.screen)
        
        draw.draw_plants() # Draw plants on the screen
        draw.draw_players() # Draw players on the screen

        # Draw text
        draw.draw_text_with_border( # Version text
            runtime_values.screen, font_renderer, f"SFG {version_text}!  {runtime_values.lang['guid']}", WHITE, BLACK, 2, pygame.math.Vector2(10, 10))
        draw.draw_text_with_border( # Coordinates
            runtime_values.screen, font_renderer, str(runtime_values.players[0].get_tile_pos()), WHITE, BLACK, 2, pygame.math.Vector2(850, 35))
        draw.draw_text_with_border( # Inventory
            runtime_values.screen, font_renderer, "inventory : "+str(runtime_values.players[0].inventory), WHITE, BLACK, 2, pygame.math.Vector2(10, 35))
        draw.draw_text_with_border( # Selected item
            runtime_values.screen, font_renderer, "select : "+runtime_values.lang["items"][runtime_values.players[0].handle_item.name], WHITE, BLACK, 2, pygame.math.Vector2(10, 70))
    
        runtime_values.screen.blit(imgs.img("mus"),musPos) # Draw the mouse cursor

        # Process keyboard inputs
        keyinput.process()

        # Move the player in the current direction and update the farm's state
        runtime_values.players[0].move(runtime_values.my_dir, df)
        farm.grow_plants()

        # Update the screen
        pygame.display.update()

    # Log that the program has quit and save the log file
    runtime_values.logs.info("quit")
    runtime_values.logs.save()

    # Quit the game
    pygame.quit()