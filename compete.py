#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 4/8/19 3:28 PM
# @Author  : xiaowa
from collections import defaultdict
from tictac import TicTac
from player import RandomPlayer, InteractivePlayer
from tictac import TicTac
from player import RandomPlayer, MCSTPlayer
from game_base import do_expand, get_valid_action_list, transform, get_blank_board, state2key
from strategy_base import random_strategy
from mcst import MCST, Node, load_mcst
from conf import BLACK
from utils import get_now_str

compete_num = 5

if __name__ == '__main__':
    score_board = defaultdict(int)
    game = TicTac()
    # mcst = MCST(TicTac.get_valid_action_list, transform, TicTac.judge, random_strategy)
    # mcst = load_mcst("mcst-500")
    mcst = load_mcst("mcst-1000-20190411-18:00:40")
    mcst_player1 = MCSTPlayer("mcst-player1", mcst)
    mcst_player2 = MCSTPlayer("mcst-player2", mcst)

    random_player = RandomPlayer("random_player")
    interactive_player = InteractivePlayer("interactive_player")

    game.add_player(mcst_player1)
    # game.add_player(random_player)
    # game.add_player(mcst_player2)
    game.add_player(interactive_player)
    game.start()

    for c in range(compete_num):
        print("compete {}".format(c))
        game.reset()
        win = game.start()
        score_board[win] += 1
    print("final result: {}".format(score_board))

    print("storing model....")
    name = "mcst-{0}-{1}".format(compete_num, get_now_str())
    mcst.store(name)
