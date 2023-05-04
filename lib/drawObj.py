import lib.draw as draw
import lib.runtime_values as runtime_values
import lib.imgs as imgs
import lib.block.block_list as block_list
import lib.plants.plants_list as plants_list
from lib import keyinput
from lib import chat
import pygame

version_text = f"{runtime_values.version[0]} {runtime_values.version[1]}.{runtime_values.version[2]}.{runtime_values.version[3]}"
font_renderer = runtime_values.font
SKYBLUE = pygame.Color(113, 199, 245)
BLACK = pygame.Color(0, 0, 0)
WHITE = pygame.Color(255, 255, 255)

def drawObj():
            musPos: tuple = pygame.mouse.get_pos()
    # 글시
            draw.draw_text_with_border( # 버전명
                runtime_values.screen, font_renderer,
                f"SFG {version_text}!  {runtime_values.lang['guid']}",
                WHITE, BLACK, 2, pygame.math.Vector2(10, 10))
            
            draw.draw_text_with_border( # 좌표
                runtime_values.screen, font_renderer,
                f"{runtime_values.players[0].get_tile_pos().x} {runtime_values.players[0].get_tile_pos().y}",
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
                
            if runtime_values.players[0].handle_item.name == "VITAMIN" or runtime_values.players[0].handle_item in block_list.block_list:
                draw.draw_text_with_border( # 아이템 겟수
                    runtime_values.screen, font_renderer,
                    f"{runtime_values.lang['count']} : {runtime_values.players[0].inventory[runtime_values.players[0].handle_item.name]}",
                    WHITE, BLACK, 2, pygame.math.Vector2(10, 60))
                
            draw.draw_text_with_border( # 돈
                runtime_values.screen, font_renderer,
                f"{runtime_values.lang['gold']} : {runtime_values.players[0].inventory['gold']}",
                WHITE, BLACK, 2, pygame.math.Vector2(10, 85))
            
            # ui
            runtime_values.screen.blit(imgs.img("item_bar"), [28*32-(256-64),20*32-32])

            # itmebar item
            count = 0
            for i in range(32,-256,-32):
                try: # TODO: 빈칸을 선택할 경우 none을 선택하게 변경, 한게가 없어지면 뒤로 밀려나게 하기
                    if runtime_values.players[0].inventory[f"{plants_list.plants_list[count].name}_seed"] > 0:
                        runtime_values.screen.blit(plants_list.plants_image[count], [28*32+i,20*32-32])
                    count+=1
                except:break
            del count
            runtime_values.screen.blit(imgs.img("item_bar_select"),[28*32-keyinput.select_bar*32+64,20*32-32])

            runtime_values.screen.blit(imgs.img("mus"),musPos) # 마우스 커서

            # 채팅 드로우
            draw.draw_text_with_border( # 
            runtime_values.screen, font_renderer,
            f"{chat.chat_list[-1][0]} : {chat.chat_list[-1][1]}",
            WHITE, BLACK, 2, pygame.math.Vector2(10, 576))