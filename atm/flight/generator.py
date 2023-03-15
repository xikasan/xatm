# -*- coding: utf-8 -*-

import numpy as np
import xtools as xt
from typing import List, Union

from .flight import Flight
from .scenario import Scenario, ScenarioIterator
from .category import Category
from .operation import Operation, OperationMode
from ..utility.random import poisson_interval


FL = List[Flight]


class ScenarioGenerator:

    def __init__(self, parameter: Union[xt.Config, dict]):
        if isinstance(parameter, dict):
            parameter = xt.Config(parameter)
        self._parameter = parameter
        self._interval: float = 1 / parameter.interval
        self._window: int = parameter.window
        self._mode: OperationMode = OperationMode.get(
            "mix" if not hasattr(parameter, "mode") else parameter.mode
        )
        self._category: Category = Category.standard(
            "recat" if not hasattr(parameter, "standard") else parameter.standard
        )

    def __call__(self, num_generate: int) -> Scenario:
        # time window
        intervals = poisson_interval(self._interval, size=num_generate).astype(int)
        times_de = np.cumsum(intervals)
        times_to = np.ones_like(times_de) * self._window + times_de

        # mode
        if self._mode == OperationMode.M:
            operations = np.random.choice(
                [o for o in Operation],
                num_generate, replace=True
            )
        else:
            operations = np.array([self._mode,] * num_generate)

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


class RealTimeScenarioGenerator:

    def __init__(self, parameter: Union[xt.Config, str]):
        if isinstance(parameter, str):
            parameter = xt.Config(parameter)
        self._parameter: xt.Config = parameter
        self.time: int = 0
        self.num_generated: int = 0

        self._next_vol: Flight = self._generate_next()

    def reset(self):
        self.time = 0
        self.num_generated = 0

    def __call__(self, time: int):
        pass

    def _generate_next(self):
        return Flight("", 1, 2, Operation.A, Category.get("recat").A)


