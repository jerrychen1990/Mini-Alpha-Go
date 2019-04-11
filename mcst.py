#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 4/8/19 3:43 PM
# @Author  : xiaowa
from game_base import do_expand, get_valid_action_list, transform, get_blank_board, state2key
from tictac import TicTac
from conf import DRAW
from strategy_base import random_strategy
from conf import BLANK, BLACK
import math
from log_utils import logger
import codecs
import _pickle as pickle


def search_add(node_dict, board, piece):
    key = state2key(board, piece)
    if key not in node_dict.keys():
        n = Node(board, piece)
        node_dict[key] = n
    return node_dict[key]


class Node:
    def __init__(self, board, piece):
        self.board = board
        self.piece = piece
        self.child_dict = {}
        self.is_expand = False
        self.win = 0
        self.draw = 0
        self.loss = 0
        self.visit = 0

    def expand(self, node_dict, action_func, transform_func):
        if not self.is_expand:
            action_list = action_func(self.board, self.piece)
            if action_list:
                action_node_list = [(a, transform_func(self.board, self.piece, a)) for a in action_list]
                for action, (next_board, next_piece) in action_node_list:
                    tmp_node = search_add(node_dict, next_board, next_piece)
                    self.child_dict[action] = tmp_node
                self.is_expand = True
        return self.is_expand

    def get_win_score(self):
        if self.visit == 0:
            return 0.5
        return (self.win * 1.0 + self.draw * .5) / self.visit

    def get_loss_score(self):
        if self.visit == 0:
            return 0.5
        return (self.loss * 1.0 + self.draw * .5) / self.visit

    def get_rare_score(self, parent, smooth=1, c=1.):
        rare_score = c * math.sqrt(math.log2(parent + smooth) / (self.visit + smooth))
        return rare_score

    def get_explore_score(self, parent, smooth=1, c=1.):
        loss_score = self.get_loss_score()
        rare_score = self.get_rare_score(parent, smooth, c)
        return loss_score + rare_score

    def get_believe_score(self):
        return math.log2(self.visit + 1)

    def get_select_score(self):
        loss_score = self.get_loss_score()
        believe_score = self.get_believe_score()
        return loss_score * believe_score

    def get_score_detail_str(self):
        return "{win}|{draw}|{loss}|{visit},wr:{wr:.2f}, lr:{lr:.2f}, blv:{blv:.2f},  sel:{sel:.2f}".format(
                win=self.win, loss=self.loss, draw=self.draw, visit=self.visit,
                wr=self.get_win_score(), lr=self.get_loss_score(),
                blv=self.get_believe_score(), sel=self.get_select_score())

    def get_next(self, strategy='explore'):
        parent = self.visit
        score_list = [(action, n.get_explore_score(parent), n.get_select_score(), n.get_score_detail_str(),
                       n.get_rare_score(parent)) for
                      action, n in self.child_dict.items()]
        if strategy == 'explore':
            logger.debug("explore for node\n {}".format(self))
            sort_list = sorted(score_list, key=lambda x: x[1], reverse=True)
            detail_list = [(e[0], e[1], e[4], e[3]) for e in sort_list]
        else:
            logger.debug("select for node\n {}".format(self))
            sort_list = sorted(score_list, key=lambda x: x[2], reverse=True)
            detail_list = [(e[0], e[2], e[3]) for e in sort_list]
        logger.debug(detail_list)
        next_action = sort_list[0][0]
        next_node = self.child_dict[next_action]
        return next_action, next_node

    def update(self, rs):
        self.visit += 1
        if rs == DRAW:
            self.draw += 1
        else:
            if rs == self.piece:
                self.win += 1
            else:
                self.loss += 1

    def __repr__(self):
        return state2key(self.board, self.piece)

    def __str__(self):
        return self.__repr__()


class MCST:
    def __init__(self, action_func, transform_func, judge_func, simulation_func):
        self.node_dict = {}
        self.action_func = action_func
        self.transform_func = transform_func
        self.judge_func = judge_func
        self.simulation_func = simulation_func

    def find_state(self, board, piece):
        node = search_add(self.node_dict, board, piece)
        return node

    def selection(self, node):
        record = []
        logger.debug("selection start...")
        while node.is_expand:
            record.append(node)
            next_action, node = node.get_next()
        node.expand(self.node_dict, self.action_func, self.transform_func)
        record.append(node)
        logger.debug("selection result:\n{}".format(node))
        return node, record

    def simulation(self, node):
        logger.debug("simulation start")
        rs = self.judge_func(node.board)
        while rs is None:
            action_list = self.action_func(node.board, node.piece)
            if not action_list:
                return DRAW
            action = self.simulation_func(action_list)
            next_board, next_piece = self.transform_func(node.board, node.piece, action)
            node = self.find_state(next_board, next_piece)
            rs = self.judge_func(node.board)
        logger.debug("simulation result:{}".format(rs))
        return rs

    @staticmethod
    def back_propagation(record, rs):
        for node in record:
            node.update(rs)

    def explode_search(self, node):
        node, record = self.selection(node)
        rs = self.simulation(node)
        MCST.back_propagation(record, rs)

    def store(self, name):
        return store_mcst(self, name)


def get_path(name):
    return "model/mcst/{name}.pkl".format(name=name)


def store_mcst(mcst, name):
    path = get_path(name)
    with codecs.open(path, 'wb') as file:
        pickle.dump(mcst, file)


def load_mcst(name):
    path = get_path(name)
    with codecs.open(path, 'rb') as file:
        mcst = pickle.load(file)
        return mcst


if __name__ == '__main__':
    the_board = get_blank_board(3)
    the_root = Node(the_board, BLACK)
    the_mcst = MCST(TicTac.get_valid_action_list, transform, TicTac.judge, random_strategy)
    the_mcst.explode_search(the_root)
    the_mcst.explode_search(the_root)
    the_mcst.explode_search(the_root)

    #
    #
    # print(mcst.selection(mcst.root))
    # print(mcst.selection(mcst.root))
    # print(mcst.selection(mcst.root))
