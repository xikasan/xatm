# coding: utf-8

import numpy as np


def set_seed(seed):
    np.random.seed(seed)


def poisson_interval(interval, size=1):
    rs = -1 * np.log(np.random.rand(size)) * interval
    if size == 1:
        return rs[0]
    return rs


def random_uniform(*size):
    if len(size) == 0 or (len(size) == 1 and size[0] == 1):
        return np.random.rand() * np.pi
    return np.random.rand(*size) * 2 - 1
