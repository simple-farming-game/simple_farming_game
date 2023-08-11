from lib.plants import plants_list
from lib.block import block_list
from lib import runtime_values


def sell(plant):
    if plant in plants_list.plants_name:
        if runtime_values.players[0].inventory[plant] > 0:
            runtime_values.players[0].gold += plants_list.plants_list[
                plants_list.plants_name.index(plant)
            ].price
            runtime_values.players[0].inventory[plant] -= 1


def buy(plant):
    if plant in plants_list.plants_name:
        if (
            runtime_values.players[0].gold
            >= plants_list.plants_list[plants_list.plants_name.index(plant)].price
        ):
            runtime_values.players[0].gold -= plants_list.plants_list[
                plants_list.plants_name.index(plant)
            ].price
            try:
                runtime_values.players[0].inventory[f"{plant}_seed"] += 1
            except KeyError:
                runtime_values.players[0].inventory[f"{plant}_seed"] = 1
    if plant in block_list.block_name:
        if (
            runtime_values.players[0].gold
            >= block_list.block_list[block_list.block_name.index(plant)].price
        ):
            runtime_values.players[0].gold -= block_list.block_list[
                block_list.block_name.index(plant)
            ].price
            try:
                runtime_values.players[0].inventory[plant] += 1
            except KeyError:
                runtime_values.players[0].inventory[plant] = 1
            print("buy")
    if plant == "VITAMIN":
        if runtime_values.players[0].gold > 15:
            runtime_values.players[0].gold -= 15
            runtime_values.players[0].inventory["VITAMIN"] += 1
