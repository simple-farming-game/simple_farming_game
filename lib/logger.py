import datetime
import os
from typing import List

from lib import runtime_values


def log_custom(text: str):
    runtime_values.logs.append(f"{text}")
    print(runtime_values.logs[-1])


def log_debug(text: str):
    runtime_values.logs.append(
        f"{datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S')} - DEBUG - {text}")
    print(runtime_values.logs[-1])


def log_info(text: str):
    runtime_values.logs.append(
        f"{datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S')} - INFO - {text}")
    print(runtime_values.logs[-1])


def log_warning(text: str):
    runtime_values.logs.append(
        f"{datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S')} - WARNING - {text}")
    print(runtime_values.logs[-1])


def log_error(text: str):
    runtime_values.logs.append(
        f"{datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S')} - ERROR - {text}")
    print(runtime_values.logs[-1])


def log_critical(text: str):
    runtime_values.logs.append(
        f"{datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S')} - CRITICAL - {text}")
    print(runtime_values.logs[-1])


def save(start_time: datetime.datetime):
    try:
        os.mkdir("log")
    except FileExistsError:
        ...
    with open(f"{os.getcwd()}\\log\\{start_time.strftime('%Y-%m-%d %H-%M-%S')}.log", "w") as log_file:
        for i in runtime_values.logs:
            log_file.write(f"{i}\n")
