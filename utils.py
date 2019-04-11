#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 4/4/19 3:43 PM
# @Author  : xiaowa
import datetime


def get_now_str():
    return datetime.datetime.strftime(datetime.datetime.now(), '%Y%m%d-%H:%M:%S')


