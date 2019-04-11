#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 4/9/19 10:42 AM
# @Author  : xiaowa

import random
from game_base import tic_tac_judge_on_hot, transform


def random_strategy(action_list):
    return random.choice(action_list)



def do_simulate(board, piece, strategy_func, judge_func, transform_func):
    pass




