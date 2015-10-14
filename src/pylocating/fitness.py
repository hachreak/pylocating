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

from numpy import matrix


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
