# coding: utf-8

import numpy as np


def poisson_interval(interval, size=1):
    rs = -1 * np.log(np.random.rand(size)) / interval
    if size == 1:
        return rs[0]
    return rs
