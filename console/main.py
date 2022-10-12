from colorama import init
from colorama import Fore, Back, Style
init()

import time
# class Co:
#     BLACK = '\033[30m'
#     RED = '\033[31m'
#     GREEN = '\033[32m'
#     YELLOW = '\033[33m'
#     BLUE = '\033[34m'
#     MAGENTA = '\033[35m'
#     CYAN = '\033[36m'
#     WHITE = '\033[37m'
#     UNDERLINE = '\033[4m'
#     RESET = '\033[0m'
# class Br:
#     BLACK = '\033[90m'
#     RED = '\033[91m'
#     GREEN = '\033[92m'
#     YELLOW = '\033[93m'
#     BLUE = '\033[94m'
#     MAGENTA = '\033[95m'
#     CYAN = '\033[96m'
#     WHITE = '\033[97m'
#     END = '\033[0m'
# 출처: https://info-lab.tistory.com/230 [:: IT School :::티스토리]

def gotoxy(x,y):
    print ("%c[%d;%df" % (0x1B, y, x), end='')

while True:
    print("00000")
    print("00000")
    print("00000")
    print("00000")
    print("00000")
    gotoxy(0,5)
    print("I")
    time.sleep(0.1)
    print("\x1B[H\x1B[J")