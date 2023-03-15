
from .base import *
from ..base import Separation
from ..discrete import DiscreteSeparation
from ..pattern import SeparationPatternTable

DBS = Separation(distance_based_separation)
TBS = Separation(time_based_separation)

dTBS = DiscreteSeparation(time_based_separation)

SeparationPattern = SeparationPatternTable(time_based_separation)
