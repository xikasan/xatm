# -*- coding: utf-8 -*-

import numpy as np
import xtools as xt
from typing import Union

from atm.flight.operation import Operation, OperationMode
from atm.flight.category import Category
from atm.flight.flight import Flight
from atm.utility.random import poisson_interval


class RealTimeScenarioGenerator:

    def __init__(self, parameter: Union[xt.Config, dict]):
        if isinstance(parameter, dict):
            parameter = xt.Config(parameter)
        self._param: xt.Config = parameter

        self._mode: OperationMode = OperationMode.get(
            "mix" if not hasattr(parameter, "mode") else parameter.mode
        )
        self._category: Category = Category.standard(
            "recat" if not hasattr(parameter, "standard") else parameter.standard
        )

        self.time: int = 0
        self.next_gen_time: int = 0
        self.num_generated: int = 0

        self.reset()

    def reset(self):
        self.time = 0
        self._renew_next_gen_time()

    def _renew_next_gen_time(self):
        self.next_gen_time = self.next_gen_time + poisson_interval(1 / self._param.interval).astype(int)

    def __call__(self, dt: int = 1):
        self.time += dt

        if self.next_gen_time > self.time:
            return None

        # times
        time_de = self.next_gen_time + self._param.margin.min + np.random.randint(0, self._param.margin.shift)
        time_to = time_de + self._param.window.min + np.random.randint(0, self._param.window.shift)

        # operation
        if self._mode == OperationMode.M:
            ope = np.random.choice([o for o in Operation])
        else:
            ope = Operation.get(self._mode.symbol)

        # category
        cat = np.random.choice([c for c in self._category])

        # generate
        vol = Flight(
            "VOL{:04.0f}".format(self.num_generated+1),
            time_de, time_to, ope, cat
        )

        # parameters update
        self.num_generated += 1
        self._renew_next_gen_time()

        return vol
