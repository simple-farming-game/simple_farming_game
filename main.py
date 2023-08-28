import sys
import json
import pygame
import datetime

pygame.init()
pygame.mixer.init()

if __name__ == "__main__":
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
    from lib import ui
    from lib import defs
    from lib import drawObj
    from lib import save
    from lib import lang
    import webbrowser

    runtime_values.logs.info("end")
    runtime_values.logs.info("init...")

    runtime_values.players.append(
        player.player(
            pygame.image.load("assets/img/player.png"),
            pygame.math.Vector2(900, 100),
            runtime_values.screen,
            runtime_values.window_size,
        )
    )

    with open("data/setting.json", "r", encoding="utf8") as setting_file:  # 셋팅파일 열기
        runtime_values.setting = json.load(setting_file)
    with open(
        f"data/lang/{runtime_values.setting['lang']}.json", "r", encoding="utf8"
    ) as lang_file:  # 언어파일 열기
        runtime_values.lang = json.load(lang_file)

    runtime_values.running = True

    farm.init()

    runtime_values.logs.info("import save...")
    save.import_save()

    runtime_values.logs.info("end")

    # 버전변수
    version = runtime_values.version
    version_text = f"{version[0]} {version[1]}.{version[2]}.{version[3]}"
    del version

    runtime_values.logs.info("                     _    ___       ___")
    runtime_values.logs.info(" _ __   _____      _| | _|_ _|_ __ |_ _|")
    runtime_values.logs.info("| '_ \\ / _ \\ \\ /\\ / / |/ /| || '_ \\ | |")
    runtime_values.logs.info("| | | |  __/\\ V  V /|   < | || | | || |")
    runtime_values.logs.info("|_| |_|\\___| \\_/\\_/ |_|\\_\\___|_| |_|___| Games")
    runtime_values.logs.info(" ____         _____         ____")
    runtime_values.logs.info("/ ___|       |  ___|       / ___|")
    runtime_values.logs.info("\\___ \\       | |_         | |  _")
    runtime_values.logs.info(" ___) |      | _|         | |_| |")
    runtime_values.logs.info("|____/ imple |_|  arming   \\____|ame\n")
    runtime_values.logs.info("코드모스 참여링크 : 디코쥐쥐 codemos")

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
    musics: dict[str, str] = {
        "sfg": "assets/music/sfg.mp3",
        "windless": "assets/music/windless.mp3",  # by 루나#9444
    }
    # ui

    # 세팅
    NICK = "없음"
    pygame.display.set_caption(f"sfg {version_text}! - by newkini")
    pygame.display.set_icon(pygame.image.load("assets/img/icon.png"))
    pygame.mouse.set_visible(False)

    runtime_values.logs.info("end")

    # 게임와일
    runtime_values.logs.info("Finish Loading")

    def not_musicStart():
        runtime_values.setting["musicStart"] = not runtime_values.setting["musicStart"]

    music = ui.Btn(f"{lang.text('setting_page.music')} : {lang.text('setting_page.on')}", not_musicStart, pygame.math.Vector2(15, 5) * 32)

    def setting():
        if runtime_values.on_setting == True:
            draw.draw_text_with_border(
                runtime_values.screen,
                runtime_values.font,
                lang.text('setting_page.setting'),
                runtime_values.WHITE,
                runtime_values.BLACK,
                2,
                pygame.math.Vector2(15 * 32, 3 * 32),
            )

            music.draw()

        if runtime_values.setting["musicStart"]:
            music.text = f"{lang.text('setting_page.music')} : {lang.text('setting_page.on')}"
        else:
            music.text = f"{lang.text('setting_page.music')} : {lang.text('setting_page.off')}"

    def opening() -> None:
        text_x_pos = 0
        target_x = runtime_values.window_size[0] / 2
        while runtime_values.running:
            runtime_values.clock.tick(runtime_values.fps)
            mus_pos: tuple = pygame.mouse.get_pos()
            runtime_values.screen.fill(SKYBLUE)
            draw.draw_text_with_border(  # 좌표
                runtime_values.screen,
                font_renderer,
                "newkini",
                WHITE,
                BLACK,
                2,
                pygame.math.Vector2(text_x_pos, runtime_values.window_size[1] / 2),
            )

            if text_x_pos < 480 and 479 < text_x_pos:
                pygame.time.wait(1000)
                target_x = runtime_values.window_size[0]
            elif text_x_pos < 960 and 959 < text_x_pos:
                break
            text_x_pos += (target_x - text_x_pos) / 15

            keyinput.process(NICK)
            runtime_values.screen.blit(imgs.img("mus"), mus_pos)  # 마우스 커서
            pygame.display.update()  # 화면 업데이트
        title()

    def title():
        pygame.mixer.music.load(musics["sfg"])
        pygame.mixer.music.play()
        start = ui.Btn(
            f"{lang.text('main_page.start')}! <smile>",
            run,
            pygame.Vector2(
                runtime_values.window_size[0] / 2, runtime_values.window_size[1] / 2
            ),
        )
        codemos_btn = ui.Btn(
            lang.text("main_page.codemos"),
            lambda: webbrowser.open("https://discord.gg/codemos"),
            pygame.math.Vector2(
                runtime_values.window_size[0] / 2 - 30 * 4 + 10,
                runtime_values.window_size[1] / 2 + 25,
            ),
        )
        official_discord_btn = ui.Btn(
            lang.text("main_page.site"),
            lambda: webbrowser.open("https://newkini-dev.com/sfg"),
            pygame.math.Vector2(
                runtime_values.window_size[0] / 2 + 30 * 4 + 10,
                runtime_values.window_size[1] / 2 + 25,
            ),
        )
        github_discord_btn = ui.Btn(
            lang.text("main_page.github"),
            lambda: webbrowser.open(
                "https://github.com/simple-farming-game/simple_farming_game/"
            ),
            pygame.math.Vector2(
                runtime_values.window_size[0] / 2 - 30 * 4 + 10,
                runtime_values.window_size[1] / 2 + 50,
            ),
        )
        youtube_discord_btn = ui.Btn(
            lang.text("main_page.youtube"),
            lambda: webbrowser.open(
                "https://www.youtube.com/channel/UCa-gBibeaPPiNYl6t_3GOIw"
            ),
            pygame.math.Vector2(
                runtime_values.window_size[0] / 2 + 30 * 4 + 10,
                runtime_values.window_size[1] / 2 + 50,
            ),
        )
        story_mod = ui.Btn(
            lang.text("main_page.storymode"),
            lambda: webbrowser.open(
                "https://github.com/simple-farming-game/sfg_story_mod"
            ),
            pygame.math.Vector2(
                runtime_values.window_size[0] / 2 + 30 * 4 + 10,
                runtime_values.window_size[1] / 2 + 75,
            ),
        )

        while runtime_values.running:
            mus_pos: tuple = pygame.mouse.get_pos()
            runtime_values.screen.fill(SKYBLUE)
            keyinput.process(NICK)
            codemos_btn.draw()
            official_discord_btn.draw()
            github_discord_btn.draw()
            youtube_discord_btn.draw()
            start.draw()
            story_mod.draw()
            draw.draw_text_with_border(  # 시간
                runtime_values.screen,
                font_renderer,
                datetime.datetime.now().strftime(lang.text("main_page.date_type")),
                WHITE,
                BLACK,
                2,
                pygame.math.Vector2(10, 85),
            )
            runtime_values.screen.blit(imgs.img("mus"), mus_pos)  # 마우스 커서
            pygame.display.update()  # 화면 업데이트
    
    def run():
        pygame.mixer.music.stop()
        pygame.mixer.music.load(musics["windless"])
        pygame.mixer.music.play(-1)
        while runtime_values.running:
            d_f = runtime_values.clock.tick(runtime_values.fps) / 1000
            runtime_values.clock.tick(runtime_values.fps)

            if runtime_values.setting["musicStart"]:
                pygame.mixer.music.unpause()
            else:
                pygame.mixer.music.pause()

            # 그리기
            # 화면
            runtime_values.screen.fill(SKYBLUE)  # 화면 채우기
            draw.draw_ground(runtime_values.screen)
            # 그외
            draw.draw_plants()  # 식물
            draw.draw_players()  # 플래이어
            # ui
            drawObj.drawObj()
            draw.draw_text_with_border(  # 좌표
                runtime_values.screen,
                font_renderer,
                "축하합니다! 당신은 이스터에그를 발견하였습니다.",
                WHITE,
                BLACK,
                2,
                pygame.math.Vector2(850, 20000),
            )

            # 처리
            process.process()
            keyinput.process(NICK)
            runtime_values.players[0].move(runtime_values.my_dir, d_f)
            farm.rot_plants(runtime_values)
            setting()
            pygame.display.update()  # 화면 업데이트

    defs.var_check(runtime_values.version)
    opening()

    runtime_values.logs.info("quit")
    runtime_values.logs.info("저장중입니다...")
    save.write_save()
    runtime_values.logs.save()
    pygame.mixer.music.stop()
    pygame.quit()
    sys.exit()
