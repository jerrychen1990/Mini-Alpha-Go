#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 4/9/19 11:06 AM
# @Author  : xiaowa
from conf import BLACK, WHITE, BLANK, DRAW
from game_base import get_blank_board, judge_on_hot, is_valid_rc_piece, get_piece, put_piece, show_board
import random
import copy
from log_utils import logger


class TicTac:
    PIECE_LIST = [BLACK, WHITE]
    MAX_WRONG_NUM = 3
    PLAYER_NUM = 2
    TARGET_LEN = 3
    SIZE = 3

    def __init__(self):
        self.board = get_blank_board(TicTac.SIZE)
        self.player_list = []

    def pre_check(self):
        if len(self.player_list) != 2:
            raise Exception("invalid player num")

    def reset(self):
        self.board = get_blank_board(self.SIZE)

    @staticmethod
    def judge_on_hot(board, hr, hc):
        return judge_on_hot(board, hr, hc, TicTac.TARGET_LEN)

    @staticmethod
    def judge(board):
        for i in range(TicTac.SIZE):
            for j in range(TicTac.SIZE):
                rs = TicTac.judge_on_hot(board, i, j)
                if rs is not None:
                    return rs
        return None

    @staticmethod
    def get_valid_action_list(board, piece):
        if TicTac.judge(board) is not None:
            return []

        return [(r, c) for r in range(TicTac.SIZE) for c in range(TicTac.SIZE) if
                is_valid_rc_piece(board, r, c, piece)]

    def do_judge(self):
        return TicTac.judge(self.board)

    def add_player(self, player):
        if len(self.player_list) == TicTac.PLAYER_NUM:
            raise Exception("too many player!")
        self.player_list.append(player)

    def put_piece(self, r, c, piece):
        if get_piece(self.board, r, c) != BLANK:
            raise Exception("invalid input!")
        put_piece(self.board, piece, r, c)

    def start(self):
        self.pre_check()
        logger.info("game start...")
        random.shuffle(self.player_list)
        for player, piece in zip(self.player_list, TicTac.PIECE_LIST):
            player.set_piece(piece)

        turn = 0
        rs = None
        while rs is None:
            logger.info("round{}".format(turn + 1))
            draw_num = 0

            for player in self.player_list:
                piece = player.piece
                valid_action_list = TicTac.get_valid_action_list(self.board, piece)
                if not valid_action_list:
                    logger.info("player {} has no way to go".format(player))
                    draw_num += 1
                    continue
                logger.info("player {} to play".format(player))

                wrong_num = 0
                while wrong_num < TicTac.MAX_WRONG_NUM:
                    action = player.get_action(copy.deepcopy(self.board), valid_action_list)
                    r, c = action
                    if action in valid_action_list:
                        logger.info("player {0} put {1} to {2}".format(player, piece, action))
                        self.put_piece(r, c, piece)
                        show_board(self.board)
                        break
                    wrong_num += 1

                tmp_rs = TicTac.judge_on_hot(self.board, r, c)
                if tmp_rs is not None:
                    rs = player
                    break

            if draw_num == len(self.player_list):
                rs = DRAW
            turn += 1
        logger.info("game finish, {} win".format(rs))
        return rs


if __name__ == '__main__':
    a = get_blank_board(3)
    show_board(a)
    a[1][1] = BLACK
    show_board(a)
    game = TicTac()
    print(game.do_judge())
    put_piece(game.board, WHITE, 0, 0)
    print(game.do_judge())
    put_piece(game.board, WHITE, 1, 0)
    print(game.do_judge())
    put_piece(game.board, WHITE, 2, 0)
    print(game.do_judge())
