#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 4/11/19 10:48 AM
# @Author  : xiaowa

import logging
from utils import get_now_str
from logging import FileHandler, StreamHandler
import sys

# logger = logging.getLogger("logger")
# logger.setLevel(logging.DEBUG)
#
# now_str = get_now_str()
# detail_handler = FileHandler("logs/all" + now_str + ".log")
# detail_handler.setFormatter(logging.Formatter("[%(levelname)s]-%(message)s"))
#
# std_handler = StreamHandler(sys.stdout)
# std_handler.setFormatter(logging.Formatter("%(message)s"))
# std_handler.setLevel(logging.INFO)
#
# logger.addHandler(detail_handler)
# logger.addHandler(std_handler)

detail_handler = FileHandler("log/all" + get_now_str() + ".log")
detail_handler.setFormatter(logging.Formatter("%(asctime)s-[%(levelname)s]-%(message)s"))

std_handler = StreamHandler(sys.stdout)
std_handler.setFormatter(logging.Formatter("%(message)s"))
std_handler.setLevel(logging.INFO)


def get_log(name, level=logging.DEBUG, file_path=None, is_print=True, include_all=True):
    logger = logging.getLogger(name)
    logger.setLevel(level)
    if file_path:
        file_handler = FileHandler(file_path, mode='w')
        file_handler.setFormatter(logging.Formatter("%(asctime)s-[%(levelname)s]-%(message)s"))
        file_handler.setLevel(logging.DEBUG)
        logger.addHandler(file_handler)
    if is_print:
        logger.addHandler(std_handler)

    if include_all:
        logger.addHandler(detail_handler)
    return logger

default_logger = get_log('default', is_print=True)

