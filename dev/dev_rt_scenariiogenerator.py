# -*- coding: utf-8 -*-

import numpy as np
import xsim
import matplotlib.pyplot as plt
import matplotlib.patches as ptc

from atm.flight.operation import Operation
from atm.flight.flight import DUMMY_FLIGHT_RECAT
from atm.separation import recat

from atm.simulator.generator import RealTimeScenarioGenerator
from atm.simulator.stripe import Stripe


if __name__ == '__main__':
    dt = 1
    parameter = dict(
        interval=60,
        window=dict(
            min=int(5*60),
            shift=int(3*60),
        ),
        mode="M",
        margin=dict(
            min=1500,
            shift=int(5*60)
        ),
    )
    rgen = RealTimeScenarioGenerator(parameter)

    queue = []
    MERGIN = 10
    separation = recat.TBS

    def fcfs_assign(stripes):
        last_vol = DUMMY_FLIGHT_RECAT
        last_time = last_vol.de
        for stripe in stripes:
            vol = stripe.vol
            sep = separation(last_vol, vol)
            time = np.max([last_time + sep + MERGIN, vol.ready])

            stripe.assign_time(time)
            stripe.assign_rwy("34L")

            last_vol = vol
            last_time = time

    def draw(time, stripes):
        print("time:", time)
        time_shift = time - 5 * 60
        num_vol = len(stripes)
        height = 1
        timespan = 60  # min
        timelimit = 10 # min

        fig, ax = plt.subplots(figsize=(20, num_vol*0.5+0.5))
        for i, vol in enumerate(stripes):
            i = num_vol - i - 1
            tde = vol.de
            tto = vol.to
            window_color = "r" if vol.ope == Operation.A else "b"
            window = ptc.Rectangle(
                (tde, height*(i+0.1)), tto - tde, height*0.8, color=window_color, alpha=0.2
            )
            window_border = ptc.Rectangle(
                (tde, height*(i+0.1)), tto - tde, height*0.8, color="k", alpha=1, fill=False, linewidth=2
            )
            tasign = vol.time
            ax.plot([tasign, tasign], [i*height, (i+1)*height], color=window_color, linewidth=3)
            ax.add_patch(window)
            ax.add_patch(window_border)

        for i in range(num_vol - 1):
            vol1 = stripes[i].vol
            vol2 = stripes[i+1].vol
            tassign = stripes[i].time
            sep = separation(vol1, vol2)

            for k in range(num_vol):
                if i > k:
                    continue
                k = num_vol - k - 1
                window_sep = ptc.Rectangle(
                    (tassign, height*+k), sep, height, color="k", alpha=0.1
                )
                ax.add_patch(window_sep)

        timelimit = time + timelimit * 60
        ax.plot([time, time], [0, height*num_vol], linewidth=3, linestyle="-", color="orange")
        ax.plot([timelimit, timelimit], [0, height*num_vol], linewidth=3, linestyle="--", color="orange")
        ax.set_xlim(time_shift, time + timespan * 60)
        ax.set_ylim(0, height * num_vol)
        xticks = np.arange((time + timespan * 60) // 300 + 1) * 300
        xticks = xticks[xticks >= time_shift]
        ax.set_xticks(xticks)
        ax.set_yticks([i*height for i in range(num_vol+1)])
        plt.grid()
        plt.show()


    for time in xsim.generate_step_time(int(60*60), dt):
        queue = [vol for vol in queue if vol.time >= time - 5 * 60]

        vol = rgen(dt=dt)
        if vol is None:
            continue

        vol = Stripe(vol)
        queue.append(vol)

        fcfs_assign(queue)

        draw(time, queue)

        print("- "*60)
