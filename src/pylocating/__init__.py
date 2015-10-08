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

"""Python Object Localization."""

from __future__ import absolute_import, unicode_literals

import numpy


__version__ = "0.1.0"

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


def fitness(base, point, radius):
    """Fitness function."""
    mpoint = numpy.matrix([point, point, point])
    mbase = numpy.matrix(base)
    mradius = numpy.matrix(radius)
    difference = mbase - mpoint
    square_difference = numpy.multiply(difference, difference)
    sum_square_diff = square_difference.sum(axis=1)
    result = sum_square_diff - mradius.transpose()
    return result.sum()


class Environment(object):

    """It Contains all information shared by the particles."""


class Particle(object):

    """Particle representation."""

    def __init__(self, particleInitializer):
        """Init particle."""
        self.position = particleInitializer.initPosition()
        self.velocity = particleInitializer.initVelocity()
        self.personalBestResult = particleInitializer.initPersonalBestResult()
        self.globalBestResult = particleInitializer.initGlobalBestResult()

    def new_velocity(self):
        """Compute the new velocity."""
        pass
