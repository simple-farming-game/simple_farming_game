import time
import os
import keyboard
os.system("pip install keyboard")
print("\x1B[H\x1B[J")
map = [
    [0,0,0,0,0],
    [0,0,0,0,0],
    [0,0,0,0,0],
    [0,0,0,0,0],
    [0,0,0,0,0]
]
plyerPos=[0,0]
while True:
    map = [
    [0,0,0,0,0],
    [0,0,0,0,0],
    [0,0,0,0,0],
    [0,0,0,0,0],
    [0,0,0,0,0]
]
    map[plyerPos[0]][plyerPos[1]]="I"
    print("tester : OTTO")
    print(map[0])
    print(map[1])
    print(map[2])
    print(map[3])
    print(map[4])
    print("나가기 : esc")
    if keyboard.is_pressed("esc"):
        break
    if keyboard.is_pressed("s"):
        if 4 == plyerPos[0]:
            pass
        else:
            plyerPos[0]+=1
    if keyboard.is_pressed("w"):
        if 0 == plyerPos[0]:
            pass
        else:
            plyerPos[0]-=1
    if keyboard.is_pressed("d"):
        if 4 == plyerPos[1]:
            pass
        else:
            plyerPos[1]+=1
    if keyboard.is_pressed("a"):
        if 0 == plyerPos[1]:
            pass
        else:
            plyerPos[1]-=1
    time.sleep(0.1)
    # map[y][x]
    # print("\x1B[H\x1B[J")
    os.system("cls")