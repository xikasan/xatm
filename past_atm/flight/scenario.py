# coding: utf-8
import numpy as np
import xtools as xt
import pandas as pd
from typing import List, TypeVar, Union
from .category import Category
from .operation import Operation, OperationMode
from .flight import Flight
from ..utility.random import poisson_interval


F = List[Flight]


class Scenario:

    def __init__(self, vols: F):
        self._vols: F = vols

    def __len__(self):
        return len(self._vols)
 
    def __iter__(self):
        return ScenarioIterator(self._vols)

    def __getitem__(self, item):
        return self._vols[item]

    def to_scv(self, file_name: str) -> pd.DataFrame:
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

    def __init__(self, vols: F):
        self._vols: F = vols
        self._size: int = len(vols)
        self._iter_index: int = 0

    def __next__(self):
        if self._iter_index == self._size:
            raise StopIteration()
        ret_vol = self._vols[self._iter_index]
        self._iter_index += 1
        return ret_vol


class ScenarioGenerator:

    def __init__(self, parameters: xt.Config):
        self._params: xt.Config = parameters
        self._interval = 1 / parameters.interval
        self._window = parameters.window
        self._mode = OperationMode.get(
            "mix" if not hasattr(parameters, "mode") else parameters.mode
        )
        self._category = Category.standard(
            "recat" if not hasattr(parameters, "standard") else parameters.standard
        )

    def __call__(self, num_generate: int) -> F:
        # time window
        intervals = poisson_interval(self._interval, size=num_generate).astype(int)
        times_de = np.cumsum(intervals)
        times_to = np.ones_like(times_de) * self._window + times_de
        # mode
        if self._mode == OperationMode.A:
            operations = np.array([Operation.A, ] * num_generate)
        elif self._mode == OperationMode.D:
            operations = np.array([Operation.D, ] * num_generate)
        else:
            operations = np.random.choice(
                [o for o in Operation],
                num_generate, replace=True
            )
        # category
        categories = np.random.choice(
            [c for c in self._category],
            num_generate, replace=True
        )
        # summarize
        code_root = "VOL{:04.0f}"
        vols = [
            Flight(code_root.format(id_+1), tde, tto, ope, cat)
            for id_, (tde, tto, ope, cat) in enumerate(
                zip(times_de, times_to, operations, categories)
            )
        ]
        return Scenario(vols)
