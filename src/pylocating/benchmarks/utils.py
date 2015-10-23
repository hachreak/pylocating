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

"""Benchmark utils."""

from __future__ import absolute_import, unicode_literals

from numpy import matrix, random


def apply_noise_gauss(point, standard_deviation):
    """Add unbiased Gaussian noise to the given point.

    e.g. apply noise to the point (10, 20, 30) with a standard deviation of 4.

    .. code-block:: python

        gen = apply_noise_gauss(np.matrix([10, 20, 30]), 4)
        point = next(gen)

    :param point: given point
    :param standard_deviation: Standard deviation of Gaussian noise
    :return: the deteriorated point
    """
    return point + matrix(random.randn(*point.shape)) * standard_deviation
