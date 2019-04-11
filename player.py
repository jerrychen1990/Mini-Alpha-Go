#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 4/8/19 2:45 PM
# @Author  : xiaowa
from abc import abstractmethod
from strategy_base import random_strategy
from log_utils import logger


class IPlayer:
    def __init__(self, name):
        self.name = name
        self.piece = None

    def set_piece(self, piece):
        self.piece = piece

    @abstractmethod
    def get_action(self, board, valid_action_list):
        pass

    def __repr__(self):
        return self.name


class RandomPlayer(IPlayer):
    def __init__(self, name):
        super(RandomPlayer, self).__init__(name)

    def get_action(self, board, valid_action_list):
        return random_strategy(valid_action_list)


class InteractivePlayer(IPlayer):
    def get_action(self, board, valid_action_list):
        raw = input("input r and c:")
        r, c = [int(e) for e in raw.strip().split(" ")]
        return r, c


class MCSTPlayer(IPlayer):
    def __init__(self, name, mcst, explore_num=3):
        super(MCSTPlayer, self).__init__(name)
        self.mcst = mcst
        self.explore_num = explore_num

    def get_action(self, board, valid_action_list):
        node = self.mcst.find_state(board, self.piece)
        for i in range(self.explore_num):
            logger.debug("mcst explode search:{}".format(i))
            self.mcst.explode_search(node)
        action, next_board = node.get_next("select")
        assert action in valid_action_list
        return action
