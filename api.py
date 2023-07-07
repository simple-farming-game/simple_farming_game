from fastapi import FastAPI
from fastapi import __version__ as fastapiver
import sys

app = FastAPI()

print(f"python ver : {list(sys.version.split())[0]}/fastapi ver : {fastapiver}/sfg path : {__file__}")

@app.get("/")
def main():
    return f"python ver : {list(sys.version.split())[0]}/fastapi ver : {fastapiver}/sfg path : {__file__}"
