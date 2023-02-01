# coding: utf-8

from __future__ import annotations
from enum import Enum
from typing import Union


class Category(Enum):

    def __init__(self, id_: int, full: str):
        self._id: int = id_
        self._full: str = full

    def __str__(self) -> str:
        return self.name.upper()

    def __eq__(self, other) -> bool:
        if isinstance(other, str):
            other = self.get(other)
        assert isinstance(other, Category)
        return self._id == other._id

    @staticmethod
    def get(cat) -> Category:
        if isinstance(cat, Category):
            return cat
        if isinstance(cat, str):
            for c in Category:
                if cat == c.name or cat == c.full:
                    return c
        raise ValueError()

    @staticmethod
    def standard(std: str) -> Category:
        std = std.upper()
        if std == "FAA":
            return CategoryFAA
        if std == "RECAT":
            return CategoryRECAT

    @property
    def symbol(self) -> str:
        return self.name.upper()

    @property
    def full(self) -> str:
        return self._full.upper()


class CategoryFAA(Category):

    # J = (11, "super")
    H = (12, "heavy")
    L = (13, "large")
    S = (14, "small")


class CategoryRECAT(Category):

    A = (1, "super-heavy")
    B = (2, "upper-heavy")
    C = (3, "lower-heavy")
    D = (4, "upper-medium")
    E = (5, "lower-medium")
    F = (6, "light")
