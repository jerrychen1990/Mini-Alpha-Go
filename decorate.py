#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 4/12/19 4:59 PM
# @Author  : xiaowa
import time
from collections import defaultdict


def cal_time(record, key):
    def decorator(func):
        def wrapper(*args, **kwargs):
            start = time.time()
            rs = func(*args, **kwargs)
            end = time.time()
            cost_time = end - start
            if key in record.keys():
                record[key]["num"] += 1
                record[key]["time"] += cost_time
            else:
                record[key] = dict(num=1, time=cost_time)
            return rs
        return wrapper

    return decorator


    # record = dict()
    # key = "add"


    # @cal_time(record, key)
    # def add(a, b):
    #     print(a + b)

    #
    # for i in range(10):
    #     add(i, i+1)
    #
    # print(record)
