# -*- coding: utf-8 -*-
#
# This file is part of pysenslog.
# Copyright 2015 Leonardo Rossi <leonardo.rossi@studenti.unipr.it>.
#
# pysenslog is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option) any
# later version.
#
# pysenslog is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with pysenslog.  If not, see <http://www.gnu.org/licenses/>.

"""Parameters Matrix generator."""

from __future__ import absolute_import, unicode_literals

import itertools


def parameter_values(start, step, end):
    """Generate a list of all possible values of a numeric parameter.

    e.g. generate all combination for cognition (0<c<3) with a step of 0.5.

    .. code-block:: python

        print parameter_values(start=0, step=0.5, end=3)

    :param start: initial value
    :param step: step from each value
    :param end: final value
    """
    values = [start]
    current = start
    total = int((end - start) // step)
    for i in range(total):
        current = current + step
        values.append(current)
    return values


def parameters_matrix(config):
    """Generate a matrix with all configurations.

    e.g. generate all combination for cognition (0<c<3) and social (0<s<3)
         with a step of 0.5.

    .. code-block:: python
        config = [
            {"start": 0, "step": 0.5, "end": 3},
            {"start": 0, "step": 0.5, "end": 3},
        ]
        print list(parameters_matrix(config))

    :param config: configuration for each parameter (start, step, end)
    :return matrix of configurations
    """
    values = []
    for i in config:
        values.append(parameter_values(**i))
    return itertools.product(*values)
