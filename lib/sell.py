from lib.plants import plants_list
from lib import runtime_values

def sell(plant: plants_list.plants_type):
    runtime_values.players[0].inventory["gold"] += plant.price
    runtime_values.players[0].inventory[f"{plant.name}"] -= 1