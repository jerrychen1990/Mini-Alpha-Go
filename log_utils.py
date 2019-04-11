#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 4/11/19 10:48 AM
# @Author  : xiaowa

import logging
from utils import get_now_str
from logging import FileHandler, StreamHandler
import sys

logger = logging.getLogger("logger")
logger.setLevel(logging.DEBUG)

now_str = get_now_str()
detail_handler = FileHandler("logs/all" + now_str + ".log")
detail_handler.setFormatter(logging.Formatter("[%(levelname)s]-%(message)s"))

std_handler = StreamHandler(sys.stdout)
std_handler.setFormatter(logging.Formatter("%(message)s"))
std_handler.setLevel(logging.INFO)

logger.addHandler(detail_handler)
logger.addHandler(std_handler)
