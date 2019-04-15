#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 4/8/19 3:59 PM
# @Author  : xiaowa
from conf import BLANK, BLACK, WHITE, DRAW, PIECE_DICT
import copy
from log_utils import get_log, default_logger
import random
from bitarray import _bitarray
import bitarray
from utils import flatmap


def get_blank_board(size, blank=BLANK):
    board = [copy.copy([BLANK] * size) for i in range(size)]
    return board


def get_board_show_str(board):
    rs = ""
    for line in board:
        rs += " ".join(line)
        rs += "\n"
    return rs


def show_board(board, logger=default_logger):
    show_str = get_board_show_str(board)
    logger.info("current board:")
    logger.info("\n" + show_str)


def is_valid_rc(board, r, c):
    return 0 <= r < len(board) and 0 <= c < len(board)


def is_valid_rc_piece(board, r, c, piece):
    return is_valid_rc(board, r, c) and board[r][c] == BLANK


def put_piece(board, piece, r, c):
    board[r][c] = piece


def get_piece(board, r, c):
    if not is_valid_rc(board, r, c):
        return None
    return board[r][c]


def judge_on_hot(board, hr, hc, target_len):
    piece = board[hr][hc]
    direction_list = [[(-1, 0), (1, 0)], [(0, -1), (0, 1)], [(-1, -1), (1, 1)], [(-1, 1), (1, -1)]]
    if piece == BLANK:
        return None
    for direction_group in direction_list:
        tmp = 1 + sum([get_direction_num(board, hr, hc, piece, d) for d in direction_group])
        if tmp >= target_len:
            return piece

    return None


def get_direction_num(board, r, c, piece, direction):
    rs = 0
    while True:
        r += direction[0]
        c += direction[1]
        if piece == get_piece(board, r, c):
            rs += 1
        else:
            break
    return rs


def state2key(board, piece):
    return piece + "\n" + get_board_show_str(board)


def state2key_small(board, piece):
    bit_str = "".join(flatmap(board, lambda x: PIECE_DICT[x]))
    bit_str = PIECE_DICT[piece] + bit_str
    return bitarray.bitarray(bit_str)


def key2state(key):
    tmp = key.split("\n")
    piece = tmp[0]
    board = [e.split[" "] for e in tmp[1:]]
    return board, piece

# def key2state_small(key):








def is_valid_action(board, action, piece):
    r, c = action
    return is_valid_rc_piece(board, r, c, piece)


def get_valid_action_list(board, piece):
    size = len(board)
    return [(r, c) for r in range(size) for c in range(size) if
            is_valid_action(board, (r, c), piece)]


def transform_piece(piece):
    return BLACK if piece == WHITE else WHITE


def transform(board, piece, action):
    next_piece = transform_piece(piece)
    next_board = copy.deepcopy(board)
    put_piece(next_board, piece, *action)
    return next_board, next_piece


def do_expand(board, piece, action_func, transform_func):
    action_list = action_func(board, piece)
    rs_dict = dict([(a, transform_func(board, piece, a)) for a in action_list])
    return rs_dict


def tic_tac_judge_on_hot(board, action):
    return judge_on_hot(board, *action, 3)


class LineGame(object):
    PIECE_LIST = [BLACK, WHITE]
    MAX_WRONG_NUM = 3
    PLAYER_NUM = 2
    TARGET_LEN = 3
    SIZE = 3

    def __init__(self, silent=False):
        self.board = get_blank_board(self.SIZE)
        self.player_list = []
        class_name = type(self).__name__
        self.logger = get_log(class_name, file_path="log/{}.log".format(class_name), is_print=not silent)

    def pre_check(self):
        if len(self.player_list) != self.PLAYER_NUM:
            self.logger.error("invalid player num")
            raise Exception("invalid player num")

    def reset(self):
        self.board = get_blank_board(self.SIZE)

    @classmethod
    def judge_on_hot(cls, board, hr, hc):
        return judge_on_hot(board, hr, hc, cls.TARGET_LEN)

    @classmethod
    def judge(cls, board):
        for i in range(cls.SIZE):
            for j in range(cls.SIZE):
                rs = cls.judge_on_hot(board, i, j)
                if rs is not None:
                    return rs
        return None

    @classmethod
    def get_valid_action_list(cls, board, piece):
        if cls.judge(board) is not None:
            return []

        return [(r, c) for r in range(cls.SIZE) for c in range(cls.SIZE) if
                is_valid_rc_piece(board, r, c, piece)]

    def do_judge(self):
        return self.judge(self.board)

    def add_player(self, player):
        if len(self.player_list) == self.PLAYER_NUM:
            raise Exception("too many player!")
        self.player_list.append(player)

    def put_piece(self, r, c, piece):
        if get_piece(self.board, r, c) != BLANK:
            raise Exception("invalid input!")
        put_piece(self.board, piece, r, c)

    def start(self):
        self.pre_check()
        self.logger.info("game start...")
        random.shuffle(self.player_list)
        for player, piece in zip(self.player_list, self.PIECE_LIST):
            player.set_piece(piece)

        turn = 0
        rs = None
        while rs is None:
            self.logger.info("round{}".format(turn + 1))
            draw_num = 0

            for player in self.player_list:
                piece = player.piece
                valid_action_list = self.get_valid_action_list(self.board, piece)
                if not valid_action_list:
                    self.logger.info("player {} has no way to go".format(player))
                    draw_num += 1
                    continue
                self.logger.info("player {} to play".format(player))

                wrong_num = 0
                while wrong_num < self.MAX_WRONG_NUM:
                    action = player.get_action(copy.deepcopy(self.board), valid_action_list)
                    r, c = action
                    if action in valid_action_list:
                        self.logger.info("player {0} put {1} to {2}".format(player, piece, action))
                        self.put_piece(r, c, piece)
                        show_board(self.board, self.logger)
                        break
                    wrong_num += 1

                tmp_rs = self.judge_on_hot(self.board, r, c)
                if tmp_rs is not None:
                    rs = player
                    break

            if draw_num == len(self.player_list):
                rs = DRAW
            turn += 1
        self.logger.info("game finish, {} win".format(rs))
        return rs


class TicTac(LineGame):
    TARGET_LEN = 3
    SIZE = 3

    def __init__(self, silent=False):
        return super(TicTac, self).__init__(silent)


class FiveGo(LineGame):
    TARGET_LEN = 4
    SIZE = 7

    def __init__(self, silent=False):
        return super(FiveGo, self).__init__(silent)
