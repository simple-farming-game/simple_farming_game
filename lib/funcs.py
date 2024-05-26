import json
import pygame


def to_json(obj):
    return str(obj)


def list_filter(lst, value_to_exclude):
    # 주어진 리스트에서 특정 값이 제외된 새로운 리스트 생성
    filtered_list = [idx for idx, val in enumerate(lst) if val != value_to_exclude]
    return filtered_list
