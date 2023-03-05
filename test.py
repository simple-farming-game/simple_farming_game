import pygame
import typing
import lib.plants.plants_list
import lib.plants.rice

sample_rice = lib.plants.rice.rice(pygame.image.load("assets/img/player.png"),
                                   pygame.math.Vector2(0, 0),
                                   pygame.display.set_mode((0, 1))
                                   )
print(
    isinstance(sample_rice, lib.plants.plants_list.plants_list)  # type: ignore
    # sample_rice
    # in
    # lib.plants.plants_list.plants_list
)
# a = typing.List[lib.plants.plants_list.plants_type] = [
#     # sample_rice
# ]

# print(lib.plants.plants_list.plants_list[1].name)
