
from fastapi import FastAPI
from fastapi import __version__ as fastapiver
import main as game
import sys

app = FastAPI()

print(f"python ver : {list(sys.version.split())[0]}/fastapi ver : {fastapiver}/sfg path : {__file__}")

@app.get("/")
def main():
    return f"python ver : {list(sys.version.split())[0]}/fastapi ver : {fastapiver}/sfg path : {__file__}"

@app.get("/spp")
def set_player_pos(x, y):
    game.spp(x, y)
    return f"python ver : {list(sys.version.split())[0]}/fastapi ver : {fastapiver}/sfg path : {__file__}"