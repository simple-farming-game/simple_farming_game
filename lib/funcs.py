import json
import pygame


def to_json(obj):
    return str(obj)


def last_index_except(lst, value_to_exclude):
    # 주어진 리스트에서 특정 값이 제외된 새로운 리스트 생성
    filtered_list = [idx for idx, val in enumerate(lst) if val != value_to_exclude]

    # 새로운 리스트의 마지막 요소의 인덱스 반환
    if filtered_list:
        return filtered_list[-1]
    else:
        return -1
