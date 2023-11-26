# -*- coding: utf-8 -*-

from typing import Callable, Dict, Optional, Tuple
from ..flight.category import Category
from ..flight.flight import Flight
from ..flight.operation import Operation


class Separation:

    def __init__(self, data: Dict[str, Dict]):
        self._table: Dict = data["table"]
        self._index: Dict[str, bool] = data["index"]
        self._call_func: Callable = self.retrievers[self.operation_index()]

    def __call__(self, leader: Flight, follower: Flight) -> int:
        lc, lo = self.__to_category_and_operation(leader)
        fc, fo = self.__to_category_and_operation(follower)
        return self._call_func(lo, fo)[lc][fc]

    def _retrieve_separation_with_follower_operation(
            self, lo: Operation, fo: Operation
    ) -> Dict[str, Dict[str, int]]:
        return self._table[fo]

    def _retrieve_separation_with_leader_operation(
            self, lo: Operation, fo: Operation
    ) -> Dict[str, Dict[str, int]]:
        return self._table[lo]

    def _retrieve_separation_with_both_operation(
            self, lo: Operation, fo: Operation
    ) -> Dict[str, Dict[str, int]]:
        return self._table[lo][fo]

    def _retrieve_separation_without_operation(
            self, lo: Operation, fo: Operation
    ) -> Dict[str, Dict[str, int]]:
        return self._table

    @property
    def retrievers(self) -> Dict[Tuple[bool, bool], Callable]:
        return {
            (True, True): self._retrieve_separation_with_both_operation,
            (True, False): self._retrieve_separation_with_leader_operation,
            (False, True): self._retrieve_separation_with_follower_operation,
            (False, False): self._retrieve_separation_without_operation
        }

    def operation_index(self) -> Tuple[bool, bool]:
        return self._index["leader"], self._index["follower"]

    @staticmethod
    def __to_category_and_operation(vol) -> Tuple[Category, Operation]:
        return vol.category.symbol, vol.operation.symbol
