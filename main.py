import sys
import pygame

pygame.init()

from lib.runtime_values import *
from lib import runtime_values
from lib.runtime_values import playerc
from lib import farm
from lib import save
from lib import player
from lib import item
from lib import ui
from lib.crops.Crops import Crops
from lib.crops.crops_item import CropsItems
from lib.blocks.blocks_item import BlocksItems
from lib.blocks.Blocks import Blocks
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

logger.info("파이게임 초기화.")

ground_images: dict[farm.Tiles, pygame.Surface] = {
    farm.Tiles.DIRT: pygame.image.load("assets/img/ground/dirt.png"),
    farm.Tiles.FARMLAND: pygame.image.load("assets/img/ground/farmland.png"),
    farm.Tiles.WATER_FARMLAND: pygame.image.load(
        "assets/img/ground/water_farmland.png"
    ),
}

pygame.display.set_caption(f"sfg {ver_text} by newkini")
pygame.display.set_icon(pygame.image.load("assets/img/icon.png"))

if not save.import_save():
    playerc.inventory = [item.Item(item.Items.NONE, 1) for _ in range(0, 8)]
    for i, j in enumerate(item.Items):
        playerc.inventory[i] = item.Item(j, 1)
    playerc.inventory[len(item.Items) - 1] = item.Item(CropsItems.RICE, 1)
    playerc.inventory[len(item.Items) - 1] = item.Item(BlocksItems.SHOP, 1)

while is_running:
    dt: float = clock.tick(100) / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

        for line in farm.tile_map:
            for tile in line:
                if isinstance(tile, Crops):
                    if event.type == tile.GROW_EVENT:
                        tile.grow()

        if event.type == pygame.KEYDOWN:
            match event.key:
                case pygame.K_LEFT:
                    if player_dir == player.Direction.STOP:
                        player_dir = player.Direction.LEFT
                    if player_dir == player.Direction.UP:
                        player_dir = player.Direction.UP_LEFT
                    if player_dir == player.Direction.DOWN:
                        player_dir = player.Direction.DOWN_LEFT
                case pygame.K_RIGHT:
                    if player_dir == player.Direction.STOP:
                        player_dir = player.Direction.RIGHT
                    if player_dir == player.Direction.UP:
                        player_dir = player.Direction.UP_RIGHT
                    if player_dir == player.Direction.DOWN:
                        player_dir = player.Direction.DOWN_RIGHT
                case pygame.K_UP:
                    if player_dir == player.Direction.STOP:
                        player_dir = player.Direction.UP
                    if player_dir == player.Direction.LEFT:
                        player_dir = player.Direction.UP_LEFT
                    if player_dir == player.Direction.RIGHT:
                        player_dir = player.Direction.UP_RIGHT
                case pygame.K_DOWN:
                    if player_dir == player.Direction.STOP:
                        player_dir = player.Direction.DOWN
                    if player_dir == player.Direction.LEFT:
                        player_dir = player.Direction.DOWN_LEFT
                    if player_dir == player.Direction.RIGHT:
                        player_dir = player.Direction.DOWN_RIGHT
                case pygame.K_d:
                    if playerc.handle_item == item.Items.HOE:
                        playerc.farm_tile(playerc.tile_pos())
                    elif playerc.handle_item == item.Items.SICKLE:
                        playerc.harvest_crops(playerc.tile_pos())
                    elif (
                        isinstance(playerc.handle_item, CropsItems)
                        and farm.tile_map[int(playerc.tile_pos().x)][
                            int(playerc.tile_pos().y)
                        ]
                        == farm.Tiles.FARMLAND
                    ):
                        playerc.plant_crops()
                    elif (
                        isinstance(playerc.handle_item, BlocksItems)
                        and farm.tile_map[int(playerc.tile_pos().x)][
                            int(playerc.tile_pos().y)
                        ]
                        == farm.Tiles.DIRT
                    ):
                        playerc.put_block()

                case pygame.K_SLASH:
                    print(playerc.inventory[runtime_values.select_inventory])
                    print(runtime_values.select_inventory)
        if event.type == pygame.KEYUP:
            match event.key:
                case pygame.K_LEFT:
                    if player_dir == player.Direction.LEFT:
                        player_dir = player.Direction.STOP
                    if player_dir == player.Direction.UP_LEFT:
                        player_dir = player.Direction.UP
                    if player_dir == player.Direction.DOWN_LEFT:
                        player_dir = player.Direction.DOWN
                case pygame.K_RIGHT:
                    if player_dir == player.Direction.RIGHT:
                        player_dir = player.Direction.STOP
                    if player_dir == player.Direction.UP_RIGHT:
                        player_dir = player.Direction.UP
                    if player_dir == player.Direction.DOWN_RIGHT:
                        player_dir = player.Direction.DOWN
                case pygame.K_UP:
                    if player_dir == player.Direction.UP:
                        player_dir = player.Direction.STOP
                    if player_dir == player.Direction.UP_LEFT:
                        player_dir = player.Direction.LEFT
                    if player_dir == player.Direction.UP_RIGHT:
                        player_dir = player.Direction.RIGHT
                case pygame.K_DOWN:
                    if player_dir == player.Direction.DOWN:
                        player_dir = player.Direction.STOP
                    if player_dir == player.Direction.DOWN_LEFT:
                        player_dir = player.Direction.LEFT
                    if player_dir == player.Direction.DOWN_RIGHT:
                        player_dir = player.Direction.RIGHT

    screen.fill(SKYBLUE)

    tile_pos = pygame.math.Vector2(0, 0)
    for line in farm.tile_map:
        for tile in line:
            screen.blit(ground_images[farm.Tiles.DIRT], tile_pos)
            if isinstance(tile, farm.Tiles):
                screen.blit(ground_images[tile], tile_pos)
            elif isinstance(tile, Crops):
                screen.blit(ground_images[farm.Tiles.FARMLAND], tile_pos)
                tile.draw()
            elif isinstance(tile, Blocks):
                tile.draw()

            tile_pos.y += 32
        tile_pos.x += 32
        tile_pos.y = 0

    # 플레이어
    playerc.draw()
    playerc.move(player_dir, dt)

    # 아이템바
    screen.blit(
        pygame.transform.scale(
            pygame.image.load("assets/img/ui/item_bar.png"), (256, 32)
        ),
        [28 * 32 - (256 - 64), 20 * 32 - 32],
    )
    for index, i in enumerate(playerc.inventory):
        if isinstance(i.item, item.Items):
            screen.blit(
                pygame.image.load(f"assets/img/items/{i.item.name.lower()}.png"),
                [28 * 32 - (256 - 64) + (index * 32), 20 * 32 - 32],
            )
        elif isinstance(i.item, CropsItems):
            screen.blit(
                pygame.image.load(f"assets/img/plants/{i.item.name.lower()}/item.png"),
                [28 * 32 - (256 - 64) + (index * 32), 20 * 32 - 32],
            )
        elif isinstance(i.item, BlocksItems):
            screen.blit(
                pygame.image.load(f"assets/img/block/{i.item.name.lower()}.png"),
                [28 * 32 - (256 - 64) + (index * 32), 20 * 32 - 32],
            )
    screen.blit(
        pygame.image.load("assets/img/ui/select_item_bar.png"),
        [28 * 32 - (256 - 64) + (runtime_values.select_inventory * 32), 20 * 32 - 32],
    )

    try:
        for i in range(1, 9):
            keys = pygame.key.get_pressed()
            if keys[getattr(pygame, f"K_{i}")]:
                runtime_values.select_inventory = i - 1
        playerc.handle_item = playerc.inventory[runtime_values.select_inventory].item
    except:
        pass

    # 기타 ui
    ui.draw_text_with_border(
        screen,
        font,
        str(playerc.handle_item.name),
        WHITE,
        BLACK,
        2,
        pygame.math.Vector2(10, 35),
    )

    ui.draw_text_with_border(
        screen, font, f"SFG {ver_text}", WHITE, BLACK, 2, pygame.math.Vector2(10, 10)
    )

    pygame.display.update()

logger.info("로그, 세이브저장, 종료를 시작합니다.")
save.write_save()
logger.save()
logger.info("저장성공!")
pygame.quit()
sys.exit()
