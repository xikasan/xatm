# -*- coding: utf-8 -*-

import numpy as np
import numpy.typing as npt
import torch
from typing import List, NewType, Union

Number = NewType("Number", Union[int, float])
Vector = NewType("Vector", Union[npt.NDArray, List[Number]])
Matrix = NewType("Matrix", Union[npt.NDArray, List[Vector]])

Tensor = NewType("Tensor", torch.Tensor)
