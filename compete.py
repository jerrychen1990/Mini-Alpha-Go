#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 4/8/19 3:28 PM
# @Author  : xiaowa
from collections import defaultdict
from player import RandomPlayer, InteractivePlayer
from player import RandomPlayer, MCSTPlayer
from game import do_expand, get_valid_action_list, transform, get_blank_board, state2key, TicTac, FiveGo
from strategy import random_strategy, line_strategy
from mcst import MCST, Node, load_mcst
from conf import BLACK
from utils import get_now_str

compete_num = 100

if __name__ == '__main__':
    score_board = defaultdict(int)
    game_type = FiveGo
    game = game_type(silent=True)
    base = 0
    mcst_name = 'mcst-fivego-simple'
    mcst = MCST(game_type.get_valid_action_list, transform, game_type.judge, line_strategy, name=mcst_name)
    # mcst = load_mcst("mcst-500")
    # mcst = load_mcst(mcst_name)
    mcst_player1 = MCSTPlayer("mcst-player1", mcst)
    mcst_player2 = MCSTPlayer("mcst-player2", mcst)

    random_player = RandomPlayer("random_player")
    interactive_player = InteractivePlayer("interactive_player")

    game.add_player(mcst_player1)
    # game.add_player(random_player)
    game.add_player(mcst_player2)
    # game.add_player(interactive_player)
    game.start()

    batch_size = 10

    for c in range(compete_num):
        if c % batch_size == 0:
            print("compete {}".format(c))
            print(score_board)
            print("storing model....")
            name = "{0}-{1}".format(mcst_name, compete_num + base)
            mcst.store(name)
        game.reset()
        win = game.start()
        score_board[win] += 1
    print("final result: {}".format(score_board))

    print(mcst.recorder)
    print("storing model....")
    name = "{0}-{1}".format(mcst_name, compete_num + base)
    mcst.store(name)
    print("compete finish")
