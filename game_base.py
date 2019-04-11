#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 4/8/19 3:59 PM
# @Author  : xiaowa
from conf import BLANK, BLACK, WHITE, DRAW
import copy
from log_utils import logger


def get_blank_board(size, blank=BLANK):
    board = [copy.copy([BLANK] * size) for i in range(size)]
    return board


def get_board_show_str(board):
    rs = ""
    for line in board:
        rs += " ".join(line)
        rs += "\n"
    return rs


def show_board(board, lg=logger):

    show_str = get_board_show_str(board)
    logger.info("current board:")
    logger.info(show_str)


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


def key2state(key):
    tmp = key.split("\n")
    piece = tmp[0]
    board = [e.split[" "] for e in tmp[1:]]
    return board, piece


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



# class LineGame:

