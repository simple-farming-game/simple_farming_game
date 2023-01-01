@echo off
POWERSHELL Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))
title y를 누르세요
echo y를 누르세요
timeout /t 3 /nobreak > NUL
choco install git
git clone https://gitlab.com/newkincode/simple_farming_game.git