import pygame
import json

if __name__ == "__main__":    
    pygame.init()
    
    # runtime values
    
    from lib import player
    from lib import runtime_values
    runtime_values.logs.info("Start Loading")
    runtime_values.logs.info("import lib...")
    from lib import imgs
    from lib import process
    from lib import draw
    from lib import keyinput
    from lib import farm
    from lib import setting
    from lib import ui
    from lib import defs
    from lib import drawObj
    import webbrowser

    runtime_values.logs.info("end")
    runtime_values.logs.info("setting runtime_values...")

    runtime_values.players.append(
        player.player(pygame.image.load("assets/img/player.png"),
        pygame.math.Vector2(900, 100),
        runtime_values.screen, runtime_values.window_size)
    )
    
    with open("data/setting.json", 'r', encoding='utf8') as setting_file: # 셋팅파일 열기
        runtime_values.setting = json.load(setting_file)
    with open(f"data/lang/{runtime_values.setting['lang']}.json", 'r', encoding='utf8') as lang_file: # 언어파일 열기
        runtime_values.lang = json.load(lang_file)
        
    runtime_values.running = True

    runtime_values.logs.info("end")

    # 버전변수
    version = runtime_values.version
    version_text = f"{version[0]} {version[1]}.{version[2]}.{version[3]}"
    del version

    runtime_values.logs.info(f"                     _    ___       ___")
    runtime_values.logs.info(f" _ __   _____      _| | _|_ _|_ __ |_ _|")
    runtime_values.logs.info(f"| '_ \\ / _ \\ \\ /\\ / / |/ /| || '_ \\ | |")
    runtime_values.logs.info(f"| | | |  __/\\ V  V /|   < | || | | || |")
    runtime_values.logs.info(f"|_| |_|\\___| \\_/\\_/ |_|\\_\\___|_| |_|___| Games")
    runtime_values.logs.info(f" ____         _____         ____")
    runtime_values.logs.info(f"/ ___|       |  ___|       / ___|")
    runtime_values.logs.info(f"\\___ \\       | |_         | |  _")
    runtime_values.logs.info(f" ___) |      | _|         | |_| |")
    runtime_values.logs.info(f"|____/ imple |_|  arming   \\____|ame\n")
    runtime_values.logs.info(f"코드모스 참여링크 : 디코쥐쥐 codemos")
    
    runtime_values.logs.info(f"V. {version_text}")

    runtime_values.logs.info("setting var...")
    # 변수
    # colors
    SKYBLUE = pygame.Color(113, 199, 245)
    BLACK = pygame.Color(0, 0, 0)
    WHITE = pygame.Color(255, 255, 255)
    # 폰트
    font_renderer = runtime_values.font
    # 노래
    musics: dict[str,pygame.mixer.Sound]={
        "sfg" : pygame.mixer.Sound("assets/music/sfg.mp3"),
        "windless" : pygame.mixer.Sound("assets/music/windless.mp3") # by 루나#9444
    }
    # ui

    # 세팅
    nick = "없음"
    pygame.display.set_caption(f"sfg {version_text}! - by newkini")
    pygame.display.set_icon(pygame.image.load('assets/img/icon.png'))
    pygame.mouse.set_visible(False)

    runtime_values.logs.info("end")

    # 게임와일
    runtime_values.logs.info("Finish Loading")

    def opening():
        x=0
        target_x = runtime_values.window_size[0]/2
        while True:
            runtime_values.clock.tick(runtime_values.fps)
            musPos: tuple = pygame.mouse.get_pos()
            runtime_values.screen.fill(SKYBLUE)
            draw.draw_text_with_border( # 좌표
                runtime_values.screen, font_renderer,
                "newkini",
                WHITE, BLACK, 2, pygame.math.Vector2(x, runtime_values.window_size[1]/2))
            
            if x < 480 and 479 < x:
                pygame.time.wait(1000)
                target_x = runtime_values.window_size[0]
            elif x < 960 and 959 < x:
                break
            x += (target_x - x)/15

            keyinput.process(nick)
            runtime_values.screen.blit(imgs.img("mus"),musPos) # 마우스 커서
            pygame.display.update()  # 화면 업데이트
        title()

    def title():
        if runtime_values.setting["musicStart"]:
            musics["sfg"].play(-1)
        start = ui.Btn("시작!", run, pygame.Vector2(runtime_values.window_size[0]/2,runtime_values.window_size[1]/2))
        codemos_btn = ui.Btn("코드모스", lambda: webbrowser.open("https://discord.gg/codemos"), pygame.math.Vector2(runtime_values.window_size[0]/2-30*4+10, runtime_values.window_size[1]/2+25))
        official_discord_btn = ui.Btn("공식디코", lambda: webbrowser.open("https://discord.gg/TpJPpHwSnM"), pygame.math.Vector2(runtime_values.window_size[0]/2+30*4+10, runtime_values.window_size[1]/2+25))
        while runtime_values.running:
            musPos: tuple = pygame.mouse.get_pos()
            runtime_values.screen.fill(SKYBLUE)
            keyinput.process(nick)
            codemos_btn.draw()
            official_discord_btn.draw()
            start.draw()
            runtime_values.screen.blit(imgs.img("mus"),musPos) # 마우스 커서
            pygame.display.update()  # 화면 업데이트
        musics["sfg"].stop()

    def run():
        musics["sfg"].stop()
        if runtime_values.setting["musicStart"]:
            musics["windless"].play(-1)
        while runtime_values.running:
            df = runtime_values.clock.tick(runtime_values.fps) / 1000
            runtime_values.clock.tick(runtime_values.fps)

            if runtime_values.setting["musicStart"]: musics["windless"].play(-1)
            else: musics["windless"].stop()

            # 그리기
            process.process()
            # 화면
            runtime_values.screen.fill(SKYBLUE)  # 화면 채우기
            draw.draw_ground(runtime_values.screen)
            # 그외
            draw.draw_plants() # 식물
            draw.draw_players() # 플래이어
            # ui
            drawObj.drawObj()

            # 처리
            keyinput.process(nick)
            runtime_values.players[0].move(runtime_values.my_dir, df)
            farm.grow_plants()
            farm.rot_plants(runtime_values)
            setting.setting()
            pygame.display.update()  # 화면 업데이트

    defs.var_check(runtime_values.version)
    opening()

    runtime_values.logs.info("quit")
    runtime_values.logs.save()
    musics["windless"].stop()
    pygame.quit()