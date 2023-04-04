from lib import farm
from lib.block import block_list

def process():
    for i in farm.tileMap:
        for j in i:
            if j in block_list.block_list:
                j.water()