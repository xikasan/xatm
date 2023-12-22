# -*- coding: utf-8 -*-

import numpy as np

from typing import Callable, List

from ..separation import recat, faa
from ..flight.scenario import Scenario
from ..flight.flight import DUMMY_FLIGHT_RECAT, DUMMY_FLIGHT_FAA
from ..separation.base import Separation

NP = np.ndarray


# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
# For single runway
#

STANDARD = recat


def calc_assign_time(indices: NP, scenario: Scenario, separation: Separation) -> NP:
    past_vol = STANDARD.DUMMY
    past_time = past_vol.ready

    times = []
    for idx in indices:
        vol = scenario[idx]
        sep_time = separation(past_vol, vol)
        time = np.max([
            vol.ready,
            past_time + sep_time
        ])
        times.append(time)

        past_vol = vol
        past_time = time

    return np.asarray(times)


def calc_delay(indices: NP, assigned_times: NP, scenario: Scenario) -> NP:
    readies = np.array([scenario[idx].ready for idx in indices])
    return assigned_times - readies


def get_due(indices: NP, scenario: Scenario) -> NP:
    return np.array([
        scenario[idx].due for idx in indices
    ])


def check_overtime(assigned_times: NP, dues: NP) -> NP:
    return np.array([
        assigned_time > due
        for assigned_time, due in zip(assigned_times, dues)
    ])


# Call this to obtain objective function for single runway
def get_obj_single_runway(scenario: Scenario, separation: Separation, penalty_coef: float = 1.0):
    def func(xs):
        times = calc_assign_time(xs, scenario, separation)
        delays = calc_delay(xs, times, scenario)
        dues = get_due(xs, scenario)
        is_overtimes = check_overtime(times, dues)
        num_overtime = np.sum(np.asarray(is_overtimes).astype(int))
        return np.mean(delays).astype(float) + penalty_coef * num_overtime
    return func


# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
# For multiple runway
#

def calc_assign_time_for_multi_runway(indices: NP, scenario: Scenario, separation: Separation) -> List[NP,]:
    return [
        calc_assign_time(indices_, scenario, separation)
        for indices_ in indices
    ]


def calc_delay_for_multi_runway(indices: NP, assigned_times: List[NP], scenario: Scenario) -> List[NP]:
    return [
        calc_delay(indices_, times_, scenario)
        for indices_, times_ in zip(indices, assigned_times)
    ]


def get_due_for_multi_runway(indices: NP, scenario: Scenario) -> List[NP]:
    return [
        get_due(indices_, scenario)
        for indices_ in indices
    ]


def check_over_time_for_multi_runway(assigned_times: List[NP], dues: List[NP]) -> List[NP]:
    return [
        check_overtime(assigned_times_, dues_)
        for assigned_times_, dues_ in zip(assigned_times, dues)
    ]


def count_num_overtime(is_overtimes: NP) -> int:
    return np.sum([
        np.sum(np.asarray(is_overtimes_).astype(int))
        for is_overtimes_ in is_overtimes
    ]).item()


# Call this to obtain objective function for multiple runway
def get_obj_multiple_runway(scenario: Scenario, separation: Separation, penalty_coef: float = 1.0) -> Callable:
    def func(xs):
        times = calc_assign_time_for_multi_runway(xs, scenario, separation)
        delays = calc_delay_for_multi_runway(xs, times, scenario)
        dues = get_due_for_multi_runway(xs, scenario)
        is_overtimes = check_over_time_for_multi_runway(times, dues)
        num_overtime = count_num_overtime(is_overtimes)

        return np.mean(np.concatenate(delays)).astype(float) + penalty_coef * num_overtime
    return func
