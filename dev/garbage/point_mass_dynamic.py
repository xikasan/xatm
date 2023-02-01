# -*- coding: utf-8 -*-

import numpy as np
import xtools as xt
import xsim
import pandas as pd
from copy import deepcopy
import matplotlib.pyplot as plt


class AirDensity:

    Ttrop = 216.65  # Temp. of tropopause : K
    beta = -0.0065  # temp. coefficient : K/m
    htrop = 11000   # threshold altitude : m
    P0 = 101325     # standard atmosphere : Pa
    g = 9.81        # gravitational acceleration : m/s^2
    # R = 8.31446262  # gas constant : m2 kg / s^2 / K / mol
    R = 287.0528    # specific gas constant

    def __init__(self, T0: float = 288.15):
        self.T0 = T0
        self.gbR = -1 * self.g / self.beta / self.R

    def __call__(self, h: float):
        return self.P(h) / self.R / self.T(h)

    def T(self, h):
        if h <= self.htrop:
            return self.T0 + self.beta * h
        return self.Ttrop

    def P(self, h):
        P = self.P0 * (self.T(h) / self.T0) ** self.gbR
        if h <= self.htrop:
            return P
        return P * np.exp(-1 * self.g * (h - self.htrop) / self.R / self.Ttrop)


class IX:
    x = 0
    y = 1
    h = 2
    v = 3
    gamma = 4
    psi = 5


def tas2cas(v, h):
    ro = AirDensity()
    k = 1.4  # heat rate of air : None
    mu = (k - 1) / k
    P = ro.P(h)

    temp = 1 + mu * v * v / ro.R / ro.T0 / 2
    temp = temp ** (1/mu) - 1
    temp = temp * P / ro.P0 + 1
    temp = temp ** mu - 1
    temp = temp * 2 * ro.P0 / mu / ro(0)
    temp = temp ** 0.5
    return temp



class PointMassAircraftA320:

    g = 9.81        # gravitational acc. : m/s^2
    S = 122.4       # wing surface area : m^2
    CL = 0.3       # Lift coefficient
    CD0 = 0.025149  # Drag coefficient as bias
    CD2 = 0.036138  # Drag coefficient for square of CL
    m = 64000       # mass : kg

    ix = IX()

    def __init__(self, dt=1.):
        # inner states
        self.v = 240.1   # ~ Mach 0.7
        self.gamma = 0.  # path angle
        self.psi = 0.    # azimuth angle
        # positions
        self.x = 0.
        self.y = 0.
        self.h = 3048   # ~ FL100 ~ 100 Cft
        self.state = np.array([
            self.x, self.y, self.h, self.v, self.gamma, self.psi
        ])
        # tools
        self.ro = AirDensity() # air density
        self.init_thrust = self.D(self.v, self.h)

        self.dt = dt

    def reset(self):
        return deepcopy(self.state)

    def __call__(self, thrust: float, roll: float):
        ix = self.ix

        def eq(state):
            h = state[ix.h]
            v = state[ix.v]
            g = state[ix.gamma]
            p = state[ix.psi]
            L = self.L(v, h)
            sing = np.sin(g)
            cosg = np.cos(g)
            return np.array([
                v * cosg * np.cos(p),  # dx
                v * cosg * np.sin(p),  # dy
                v * sing,  # dh
                (thrust - self.D(v, h)) / self.m - self.g * sing,  # dv
                (L * np.cos(roll) - self.m * self.g * cosg) / v / self.m,  # dgamma
                L * np.sin(roll) / self.m / v / cosg,  # dpsi
            ])

        dstate = xsim.no_time_rungekutta(eq, self.dt, self.state)
        self.state = dstate * self.dt
        return deepcopy(self.state)

    def D(self, v, h):
        CD = self.CD0 + self.CD2 * self.CL * self.CL
        return 0.5 * self.ro(h) * v * v * CD * self.S

    def L(self, v, h):
        return 0.5 * self.ro(h) * v * v * self.CL * self.S


if __name__ == '__main__':

    vtas = 271.39547
    vcas = tas2cas(vtas, 10668)  # FL350
    print(vcas)
    vcas = tas2cas(vtas,  3048)  # FL100
    print(vcas)
    exit()

    aircraft = PointMassAircraftA320()
    print(aircraft.ro(10668))
    exit()

    Kg = -10  # feedback coefficient

    log = xsim.Logger()
    state = deepcopy(aircraft.state)
    ix = aircraft.ix
    for t in xsim.generate_step_time(60, aircraft.dt):
        h = state[ix.h]
        dth = (h - 30480) * Kg
        log.store(
            time=t,
            state=state,
            dth=dth
        ).flush()

        state = aircraft(aircraft.init_thrust + dth, 0)

    ret = xsim.Retriever(log)
    res = pd.DataFrame(dict(
        time=ret.time(),
        x=ret.state(ix.x),
        y=ret.state(ix.y),
        h=ret.state(ix.h),
        g=ret.state(ix.gamma),
        p=ret.state(ix.psi),
        dth=ret.dth(),
    ))

    fig, axes = plt.subplots(nrows=3)
    res.plot(x="time", y="h", ax=axes[0])
    res.plot(x="time", y="g", ax=axes[1])
    res.plot(x="time", y="dth", ax=axes[2])
    plt.show()

