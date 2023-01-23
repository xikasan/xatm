# -*- coding: utf-8 -*-

from typing import Callable, Dict, Tuple
from .base import Separation


class DiscreteSeparation(Separation):

    def __init__(self, data: Dict[str, Dict], dt: int = 10):
        super().__init__(data)
        self._dt: int = dt
        self._table = self._discretize()

    def _discretize(self):
        cat_index = self.operation_index()
        return self.discretizers[cat_index](self._table)

    @property
    def discretizers(self) -> Dict[Tuple[bool, bool], Callable]:
        return {
            (True, True): self._discretize_for_double_operation,
            (True, False): self._discretize_for_single_operation,
            (False, True): self._discretize_for_single_operation,
            (False, False): self._discretize_for_no_operation,
        }

    def _discretize_for_double_operation(self, table):
        return {
            ope: self._discretize_for_single_operation(table[ope])
            for ope in table.keys()
        }

    def _discretize_for_single_operation(self, table):
        return {
            ope: self._discretize_for_no_operation(table[ope])
            for ope in table.keys()
        }

    def _discretize_for_no_operation(self, table: Dict[str, Dict[str, int]]):
        return {
            cat1: {
                cat2: self.discretize_time(table[cat1][cat2])
                for cat2 in table[cat1].keys()
            } for cat1 in table.keys()
        }

    def discretize_time(self, time: int) -> int:
        return (time + self._dt - 1) // self._dt

    def dt(self, dt: int):
        assert dt > 0
        self._table = self._discretize()

    @property
    def table(self):
        return self._table

