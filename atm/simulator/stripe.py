# -*- coding: utf-8 -*-

from atm.flight.flight import Flight


class Stripe:

    def __init__(self, vol: Flight):
        self.vol = vol
        self.rwy = None
        self.time = None
        self.via = None

    def __str__(self):
        vol = self.vol
        ret = "SFlight("
        ret += vol.code + ": "
        ret += "[{:4.0f}-{:4.0f}] ".format(vol.de, vol.to)
        ret += f"wtc:{vol.cat} ope:{vol.ope} "
        ret += f"| rwy:{self.rwy} time:{self.time}"
        if self.via is not None:
            ret += f" via:{self.via}"
        return ret

    @property
    def de(self):
        return self.vol.de

    @property
    def to(self):
        return self.vol.to

    @property
    def cat(self):
        return self.vol.cat

    @property
    def ope(self):
        return self.vol.ope

    def assign_rwy(self, rwy):
        self.rwy = rwy

    def assign_time(self, time):
        self.time = time
