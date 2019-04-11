#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 4/8/19 3:14 PM
# @Author  : xiaowa
from tictac import TicTac
from player import RandomPlayer, MCSTPlayer
from game_base import do_expand, get_valid_action_list, transform, get_blank_board, state2key
from strategy_base import random_strategy
from mcst import MCST, Node
from conf import BLACK

game = TicTac()
the_board = get_blank_board(3, 3)
mcst = MCST(TicTac.get_valid_action_list, transform, TicTac.judge, random_strategy)

mcst_player = MCSTPlayer("mcst-player", mcst)
random_player = RandomPlayer("random_player")

game.add_player(mcst_player)
game.add_player(random_player)
game.start()

mcst.store("mcst")



