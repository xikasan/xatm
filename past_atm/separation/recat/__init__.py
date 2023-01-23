# -*- coding: utf-8 -*-

from .base import *
from ..base import Separation
from ..discrete import DiscreteSeparation
from ..pattern import SeparationPatternTable

DBS = Separation(distance_based_separation_table)
TBS = Separation(time_based_separation_table)

dTBS = DiscreteSeparation(time_based_separation_table)

SeparationPattern = SeparationPatternTable(time_based_separation_table)
