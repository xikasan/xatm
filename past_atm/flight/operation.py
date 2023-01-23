# coding: utf-8

from __future__ import annotations
from enum import Enum, auto
from typing import Union


class OperationMode(Enum):

    M = (0, "MIX", "mix")
    A = (1, "ARR", "arrival")
    D = (2, "DEP", "departure")

    def __init__(self, id_: int, code: str, full: str):
        self._id: int = id_
        self._code: str = code.upper()
        self._full: str = full.upper()

    def __str__(self) -> str:
        return self.name

    def __eq__(self, other: Union[OperationMode, str]) -> bool:
        if isinstance(other, str):
            other = self.self.get(other)
        assert isinstance(other, OperationMode)
        return self._id == other._id

    @staticmethod
    def get(ope: Union[OperationMode, str]) -> OperationMode:
        if isinstance(ope, OperationMode):
            return ope
        if isinstance(ope, str):
            ope = ope.upper()
            for o in OperationMode:
                if ope == o.name or ope == o.code or ope == o.full:
                    return o
        raise ValueError()

    @property
    def symbol(self) -> str:
        return self.name.upper()

    @property
    def code(self) -> str:
        return self._code

    @property
    def full(self) -> str:
        return self._full


class Operation(Enum):
    A = (1, "ARR", "arrival")
    D = (2, "DEP", "departure")

    def __init__(self, id_: int, code: str, full: str):
        self._id: int = id_
        self._code: str = code.upper()
        self._full: str = full.upper()

    def __str__(self) -> str:
        return self.name

    def __eq__(self, other: Union[Operation, str]) -> bool:
        if isinstance(other, str):
            other = self.self.get(other)
        assert isinstance(other, OperationMode)
        return self._id == other._id

    @staticmethod
    def get(ope: Union[Operation, str]) -> Operation:
        if isinstance(ope, Operation):
            return ope
        if isinstance(ope, str):
            ope = ope.upper()
            for o in Operation:
                if ope == o.name or ope == o.code or ope == o.full:
                    return o
        raise ValueError()

    @property
    def symbol(self) -> str:
        return self.name.upper()

    @property
    def code(self) -> str:
        return self._code

    @property
    def full(self) -> str:
        return self._full
