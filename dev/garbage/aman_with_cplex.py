# -*- coding: utf-8 -*-

import numpy as np
import xtools as xt
from docplex.mp.model import Model
from typing import List, Optional, Tuple, Union

from past_atm.flight.flight import Flight
from past_atm.flight.scenario import ScenarioGenerator, Scenario
from past_atm.separation import recat
from past_atm.separation.base import Separation


def build_model(vols: Scenario, sep: Separation) -> Tuple[Model, tuple, tuple]:
    M: int = 1000  # big-M

    m = Model("AMAN")

    # define variables
    # assign time
    ts = {
        vol.code: m.integer_var(lb=vol.ready, ub=vol.due, name=f"T_{vol.code}")
        for vol in vols
    }
    # leader flag
    # y = 1 if vol1 leads vol2
    ys = {
        ix(vol1, vol2): m.binary_var(name=f"y_{vol1.code}_{vol2.code}")
        for vol1 in vols
        for vol2 in vols
        if not vol1 == vol2
    }

    # constrains
    [
        m.add_constraint(ts[ix(vol2)] >= ts[ix(vol1)] + sep(vol1, vol2) - M * (1 - ys[ix(vol1, vol2)]))
        for vol1 in vols
        for vol2 in vols
        if not vol1 == vol2
    ]

    [
        m.add_constraint(ys[ix(vol1, vol2)] + ys[ix(vol2, vol1)] == 1)
        for vol1 in vols
        for vol2 in vols
        if vol1 < vol2
    ]

    m.minimize(m.sum([
        ts[ix(vol)] - vol.ready
        for vol in vols
    ]))

    return m, ts, ys


def ix(vol1: Flight, vol2: Optional[Flight] = None) -> Union[str, Tuple[str, str]]:
    if vol2 is None:
        return vol1.code

    return vol1.code, vol2.code


if __name__ == '__main__':
    cf = xt.Config(dict(
        interval=60,
        window=int(60*20),
        category="recat",
        mode="arr",
    ))
    sg: ScenarioGenerator = ScenarioGenerator(cf)
    vols: Scenario = sg(5)

    print("Scenario:")
    print(vols.to_dataframe())
    exit()

    separation: Separation = recat.TBS

    m, ts, ys = build_model(vols, separation)
    m.print_information()
    print("Objective:")
    print(m.objective_expr)
    for i, c in enumerate(m.iter_constraints()):
        print("C{:04.0f}:".format(i), c)

    m.solve()
    m.print_solution()
    for v in m.iter_variables():
        print(v.name, ":", v.solution_value)

