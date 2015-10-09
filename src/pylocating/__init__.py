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


class Information(object):

    """Single unit of Information shareb by the particles."""

    def __init__(self, position, fitness, velocity=0):
        """Init information."""
        self.position = position
        self.fitness = fitness
        self.velocity = velocity

    def isBetterThan(self, info):
        """Check if this is better that the other iformation."""
        return self.fitness >= info.fitness

    def __eq__(self, other):
        """Test if `self` is equal to `other`."""
        return self.position == other.position and \
            self.fitness == other.fitness and self.velocity == other.velocity


class Environment(object):

    """It Contains all information shared by the particles."""

    def __init__(self):
        """Init environment."""
        self.particles = {}
        self.globalBest = Information([0, 0, 0], 0)

    def updateParticleBest(self, info):
        """Get particle best."""
        if not self.globalBest.isBetterThan(info):
            self.globalBest = info

    def register(self, particle):
        """Register new particle."""
        self.particles[particle.id] = particle

    @property
    def bestResult(self):
        """Compute realtime the new global best result."""
        max = numpy.matrix(
            [p.bestResult for p in self.particles.values()]).max()
        return list(
            filter((lambda p: p.bestResult == max),
                   self.particles.values()))[0]


class Particle(object):

    """Particle representation."""

    def __init__(self, environment, id=None, info=None):
        """Init particle."""
        self._id = id
        self.environment = environment
        self.environment.register(self)
        self.position = info.position or [0, 0, 0]
        self.velocity = info.velocity or [0, 0, 0]
        self.bestResult = info.fitness or 0

    @property
    def bestResult(self):
        """Get personal best result."""
        return self._bestResult

    @bestResult.setter
    def bestResult(self, value):
        """Set personal best result and update environment."""
        self._bestResult = value
        info = Information(
            position=self.position, fitness=self._bestResult)
        self.environment.updateParticleBest(info=info)

    @property
    def id(self):
        """Get id."""
        return self._id if self._id else str(self)

    @id.setter
    def id(self, value):
        """Set id."""
        self._id = value
