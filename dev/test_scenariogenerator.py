# -*- coding: utf-8 -*-

from atm.flight.generator import ScenarioGenerator


if __name__ == '__main__':
    parameter = dict(
        interval=60,
        window=int(60*10),
        mode="M"
    )
    sgen = ScenarioGenerator(parameter)
    vols = sgen(10)
    print(vols.to_dataframe())
