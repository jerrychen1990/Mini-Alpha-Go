#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 4/9/19 10:42 AM
# @Author  : xiaowa

import random
from game import tic_tac_judge_on_hot, transform, get_direction_num

direction_list = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, 1), (-1, 1), (1, -1)]


def random_strategy(board, piece, action_list):
    return random.choice(action_list)


def line_strategy(board, piece, action_list):
    score_list = []
    for r, c in action_list:
        score = sum([get_direction_num(board, r, c, piece, d) for d in direction_list])
        score_list.append(((r, c), score))
    action, score = max(score_list, key=lambda x: x[1])
    return action
