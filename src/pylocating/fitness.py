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

"""Python Localization Fitness functions."""

from __future__ import absolute_import, unicode_literals

from numpy import matrix, multiply

# Base matrix
#
# [x0] [y0] [z0] - position of beacon 0
# [x1] [y1] [z1] - position of beacon 1
# [x2] [y2] [z2] - position of beacon 2
#  ..   ..   ..
# [xM] [yM] [zM] - position of beacon M
#
# Radius (distance of the object from the beacon
# [r0] - from beacon 0
# [r1] - from beacon 1
# [r2] - from beacon 2
#  ..
# [rM] - from beacon M
#
# Point (selected by the Bee)
# [px] [py] [px]
#


def fitness(point, base, radius):
    """Fitness function.

    :param point: current position to evaluate (vector)
    :param base: position of M beacons (matrix: M x [X, Y, Z])
    :param radius: distance of the object computed by the M beacons (vector)
    """
    difference = base - point
    square_difference = multiply(difference, difference)
    sum_square_diff = square_difference.sum(axis=1)
    result = sum_square_diff - radius.transpose()
    return result.sum()


def fitness_numpy_adapter(point, base, radius):
    """Adapt data to numpy objects.

    e.g.
        fitness(*fitness_numpy_adapter(
            [1,2,3],
            [[1,2,3], [4,5,6], [7,8,9]],
            [1,2,3]
        ))

    :param point: python list [X, Y, Z]
    :param base: python list of list [[X, Y, Z], ... ]
    :param radius: python list [A, B, C, ... ]
    """
    mpoint = matrix([point, point, point])
    mbase = matrix(base)
    mradius = matrix(radius)
    return (mpoint, mbase, mradius)
