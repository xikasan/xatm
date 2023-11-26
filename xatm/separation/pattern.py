# -*- coding: utf-8 -*-

import numpy as np
from copy import deepcopy
from typing import Callable, Dict, Optional, Tuple
from .base import Separation
from .discrete import DiscreteSeparation
from ..flight.flight import Flight
from ..flight.operation import Operation
from ..utility.typing import Matrix

# for test
import matplotlib.pyplot as plt


class SeparationPatternTable(DiscreteSeparation):

    def __init__(self, data: Dict[str, Dict], dt: int = 10, max_window_size: int = 120):
        super().__init__(data, dt=dt)
        self.max_window_size: int = max_window_size
        self._pattern: Dict[str, Dict] = self._map()
        self._call_func: Callable = self.fetchers[self.operation_index()]

    def _map(self):
        return self.mapper[self.operation_index()](self._table)

    @property
    def fetchers(self) -> Dict[Tuple[bool, bool], Callable]:
        return {
            (True, True): self._fetch_map_with_both_operation,
            (True, False): self._fetch_map_with_leader_operation,
            (False, True): self._fetch_map_with_follower_operation,
            (False, False): self._fetch_map_without_operation,
        }

    def _fetch_map_with_both_operation(
            self, lo: Operation, fo: Operation
    ) -> Dict[str, Dict[str, int]]:
        return self._pattern[lo][fo]

    def _fetch_map_with_leader_operation(
            self, lo: Operation, fo: Operation
    ) -> Dict[str, Dict[str, int]]:
        return self._pattern[lo]

    def _fetch_map_with_follower_operation(
            self, lo: Operation, fo: Operation
    ) -> Dict[str, Dict[str, int]]:
        return self._pattern[fo]

    def _fetch_map_without_operation(
            self, lo: Operation, fo: Operation
    ) -> Dict[str, Dict[str, int]]:
        return self._pattern

    @property
    def mapper(self) -> Dict[Tuple[bool, bool], Callable]:
        return {
            (True, True): self._map_for_double_operation,
            (True, False): self._map_for_single_operation,
            (False, True): self._map_for_single_operation,
            (False, False): self._map_for_no_operation,
        }

    def _map_for_double_operation(self, table):
        return {
            ope: self._map_for_single_operation(table[ope])
            for ope in table.keys()
        }

    def _map_for_single_operation(self, table):
        return {
            ope: self._map_for_no_operation(table[ope])
            for ope in table.keys()
        }

    def _map_for_no_operation(self, table):
        return {
            cat1: {
                cat2: self.map_pattern(table[cat1][cat2])
                for cat2 in table[cat1].keys()
            } for cat1 in table.keys()
        }

    def map_pattern_ex(self, slot: int):
        d_max_win_size = self.max_window_size // self._dt
        pattern_size = 3 * d_max_win_size + 2 * slot
        padding_size = pattern_size - slot - 1
        content_size = slot + 1
        return np.array([
            sum([[0, ] * d, [1, ] * content_size, [0, ] * (padding_size - d)], [])
            for d in range(padding_size + 1)
        ])

    def map_pattern(self, slot: int):
        d_max_window_size = self.max_window_size // self._dt + 1
        block_pattern_size = d_max_window_size + slot
        content_size = slot + 1  # -1 is sub for exact assigned slot
        padding_size = block_pattern_size - content_size
        return np.array([
            sum([
                [0, ] * d_max_window_size,
                [0, ] * d,
                [1, ] * content_size,
                [0, ] * (padding_size - d),
                [0, ] * d_max_window_size
            ], [])
            for d in range(d_max_window_size)
        ])

    def reparameterize(self, dt: int = None, max_time_window: int = None):
        if dt is not None:
            self.dt(dt)
        if max_time_window is not None:
            self.max_time_window(max_time_window)
        self._pattern = self._map()

    def retrieve_table(self, vol1: Flight, vol2: Flight, discretized: Optional[bool] = False) -> Matrix:
        pattern = self(vol1, vol2)
        if not discretized:
            r1, d1 = self.__discretize_ready_and_due(vol1)
            r2, d2 = self.__discretize_ready_and_due(vol2)
        else:
            r1, d1 = vol1.ready, vol1.due
            r2, d2 = vol2.ready, vol2.due

        dmax = self.max_window_size // self._dt
        w1 = d1 - r1
        w2 = d2 - r2
        # return zeros if in out of table
        # left of table
        if d2 - r1 < 0:
            return np.zeros((w1, w2))

        # r1_, d1_ = r1 - r1 + dmax, d1 - r1 + dmax
        r2_, d2_ = r2 - r1 + dmax, d2 - r1 + dmax
        return pattern[:w1, r2_:d2_]

    def __discretize_ready_and_due(self, vol):
        r = self.discretize_time(vol.ready)
        d = self.discretize_time(vol.due)
        return r, d

    def max_time_window(self, val):
        self.max_window_size = val
