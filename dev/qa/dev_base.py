# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import xtools as xt

from scipy.linalg import block_diag
from openjij import SQASampler, SASampler

from atm.flight.generator import ScenarioGenerator
from atm.separation import recat


cf = xt.Config(dict(
    dt=10,
    num=10,
    scenario=dict(
        interval=36,
        window=300,
        mode="mix",
        standard="recat"
    )
))

pattern = recat.SeparationPattern
pattern.reparameterize(dt=cf.dt, max_time_window=cf.scenario.window)

sgen = ScenarioGenerator(cf.scenario)
vols = sgen(cf.num)

num_slot = cf.scenario.window // cf.dt
num_qubit = num_slot * cf.num

# - - - - - - - - - - - - - - - - - - - - - - - - - -
# build delay cost
delays = np.arange(num_slot).tolist()
delays = [delays, ] * cf.num
delays = sum(delays, [])
q_delay = np.diag(delays)
q_delay = q_delay / np.max(q_delay)

# - - - - - - - - - - - - - - - - - - - - - - - - - -
# build unique cost
uniques = np.eye(num_slot)
uniques = -2 * uniques + np.ones_like(uniques)
uniques = [uniques, ] * cf.num
q_unique = block_diag(*uniques)

# - - - - - - - - - - - - - - - - - - - - - - - - - -
# build separation cost
costs = []
for id1, vol1 in enumerate(vols):
    costs_row = []
    for id2, vol2 in enumerate(vols):
        if vol1 == vol2:
            costs_row.append(np.zeros((num_slot, num_slot)))
            continue
        costs_row.append(pattern.retrieve_table(vol1, vol2))
    cost_row = np.hstack(costs_row)
    costs.append(cost_row)
q_sep = np.vstack(costs)

# - - - - - - - - - - - - - - - - - - - - - - - - - -
qubo = q_delay + q_unique + q_sep
# qubo = q_delay + 2 * q_unique + 2 * q_sep
# qubo = q_unique + q_sep

# - - - - - - - - - - - - - - - - - - - - - - - - - -
# solve with QA sampler
sampler = SQASampler(num_reads=10)
sampleset = sampler.sample_qubo(qubo)
sample = sampleset.first
xs = list(sample.sample.values())
xs = np.reshape(xs, (cf.num, num_slot))
print(xs)

def discrete_time(t):
    return (t + cf.dt - 1) // cf.dt


Rs = [discrete_time(vol.ready) for vol in vols]
Ds = np.argmax(xs, axis=1)
assigned_slots = Rs + Ds
print(Rs, Ds, assigned_slots)

fig, ax = plt.subplots(figsize=(10, 10))
ax.imshow(qubo)
ds = Ds + (np.arange(len(vols)) * num_slot).astype(int) - 0.5
cs = sum([
    [
        patches.Rectangle((d1, d2), width=1, height=1, edgecolor="#ff0000", fill=False, linewidth=2)
        for d2 in ds
    ]
    for d1 in ds
], [])
[ax.add_patch(c) for c in cs]
plt.show()
print(vols.to_dataframe())
