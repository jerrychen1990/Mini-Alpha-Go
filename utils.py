#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 4/4/19 3:43 PM
# @Author  : xiaowa
import datetime
from itertools import chain


def get_now_str():
    return datetime.datetime.strftime(datetime.datetime.now(), '%Y%m%d-%H:%M:%S')


def flatten(list_of_list):
    return list(chain.from_iterable(list_of_list))


def flatmap(seq, func):
    return [func(e) for e in flatten(seq)]


if __name__ == '__main__':
    a = [1, 2, 3]
    b = flatmap(a, lambda x: [x, x * x])
    print(b)
