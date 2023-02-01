# -*- coding: utf-8 -*-

import numpy as np
import xtools as xt
import pandas as pd
from typing import List

from .category import Category
from .operation import Operation, OperationMode
from .flight import Flight
from ..utility.random import poisson_interval


FL = List[Flight]


class Scenario:

    def __init__(self, vols: FL):
        self._vols: FL = vols

    def __len__(self) -> int:
        return len(self._vols)

    def __iter__(self):
        return ScenarioIterator(self._vols)

    def __getitem__(self, item: int) -> Flight:
        return self._vols[item]

    def to_csv(self, file_name) -> pd.DataFrame:
        df = self.to_dataframe()
        df.to_csv(file_name, index=False)
        return df

    def to_dataframe(self) -> pd.DataFrame:
        return pd.DataFrame(dict(
            code=[vol.code for vol in self._vols],
            ready=[vol.de for vol in self._vols],
            due=[vol.to for vol in self._vols],
            category=[vol.cat for vol in self._vols],
            operation=[vol.ope for vol in self._vols]
        ))


class ScenarioIterator:

    def __init__(self, vols: FL):
        self._vols: FL = vols
        self._size: int = len(vols)
        self._iter_index: int = 0

    def __next__(self):
        if self._iter_index == self._size:
            raise StopIteration()
        ret_vol = self._vols[self._iter_index]
        self._iter_index += 1
        return ret_vol

