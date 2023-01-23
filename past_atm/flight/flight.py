# coding: utf-8

from typing import Union
from .category import Category
from .operation import Operation


class Flight:

    def __init__(
            self,
            code: str,
            ready_time: int,
            due_time: int,
            operation: Union[Operation, str],
            category: Union[Category, str]
    ):
        self._code = code.upper()
        assert 0 < ready_time < due_time
        self._time_de = ready_time
        self._time_to = due_time
        self._ope = Operation.get(operation)
        self._cat = Category.get(category)

    def __str__(self):
        ret = f"Flight({self.code}: [{self.de}-{self.to}] wtc:{self.cat} ope:{self.ope})"
        return ret

    def __eq__(self, other):
        if not isinstance(other, Flight):
            return False
        return self.code == other.code

    def __ne__(self, other):
        neg_ret = self.__eq__(other)
        return not neg_ret

    def __lt__(self, other):
        self.__check_type_and_raise_type_error(other)
        return self.code < other.code

    def __le__(self, other):
        return self.__lt__(other) or self.__eq__(other)

    def __gt__(self, other):
        self.__check_type_and_raise_type_error(other)
        return self.code > other.code

    def __ge__(self, other):
        return self.__gt__(other) or self.__eq__(other)

    def __hash__(self):
        return hash(self._code)

    @staticmethod
    def __check_type_and_raise_type_error(other):
        if isinstance(other, Flight):
            return
        raise TypeError("Non Flight object is tried to compare with Flight.")

    @property
    def code(self):
        return self._code

    @property
    def ready(self):
        return self._time_de

    @property
    def de(self):
        return self._time_de

    @property
    def due(self):
        return self._time_to

    @property
    def to(self):
        return self._time_to

    @property
    def operation(self):
        return self._ope

    @property
    def ope(self):
        return self._ope

    @property
    def category(self):
        return self._cat

    @property
    def cat(self):
        return self._cat


cat_faa = Category.standard("faa")
__dummy_faa = Flight("DUMMY", 1, 2, "D", cat_faa.H)
__dummy_faa._time_to = 0
__dummy_faa._time_de = -200
DUMMY_FLIGHT_FAA = __dummy_faa

cat_recat = Category.standard("recat")
__dummy_recat = Flight("DUMMY", 1, 2, "D", cat_recat.A)
__dummy_recat._time_to = 0
__dummy_recat._time_de = -200
DUMMY_FLIGHT_RECAT = __dummy_recat
