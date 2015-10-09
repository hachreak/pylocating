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

from copy import deepcopy

__version__ = "0.1.0"


class EmptyEnvironment(Exception):
    pass

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

def move(info, binfo, w, c1, c2, random):
    """Compute next position and velocity of the particle.

    :param info: information about current particle
    :param binfo: information about the particle with best fitness
    :param w: inertial weight
    :param c1: cognition parameter
    :param c2: social parameter
    :param random: randomizer object that return random diagonal matrix with
        values uniformed distributed in the interval [0,1)
    :return: new information of the particle
    """
    next_velocity = w * info.velocity + \
        c1 * random.next() * (binfo.velocity - info.velocity) + \
        c2 * random.next() * (binfo.position - info.position)
    next_position = info.position + next_velocity
    return Information(position=next_position, velocity=next_velocity,
                       fitness=info.fitness)


class Information(object):

    """Single unit of Information shareb by the particles."""

    def __init__(self, position=None, fitness=None, velocity=None):
        """Init information."""
        self.position = position if position is not None else \
            numpy.matrix([0, 0, 0])
        self.fitness = fitness or 0
        self.velocity = velocity if velocity is not None else \
            numpy.matrix([0, 0, 0])

    def isBetterThan(self, info):
        """Check if this is better that the other iformation."""
        return self.fitness >= info.fitness

    def __eq__(self, other):
        """Test if `self` is equal to `other`."""
        return (self.position == other.position).all() and \
            self.fitness == other.fitness and \
            (self.velocity == other.velocity).all()


class Environment(object):

    """It Contains all information shared by the particles."""

    def __init__(self, info=None):
        """Init environment."""
        self.particles = {}
        self.globalBest = info or Information()

    def register(self, particle):
        """Register new particle."""
        self.particles[particle.id] = particle

    @property
    def best(self):
        """Compute realtime the new global best result."""
        try:
            max = numpy.matrix(
                [p.bestResult.fitness for p in self.particles.values()]).max()
            return list(
                filter((lambda p: p.bestResult.fitness == max),
                       self.particles.values()))[0]
        except ValueError:
            raise EmptyEnvironment("""The environment is empty! """
                                   """Please insert new particles.""")


class Particle(object):

    """Particle representation."""

    def __init__(self, environment, id=None, current=None, best=None):
        """Init particle."""
        self._id = id
        self.environment = environment
        self.environment.register(self)
        self.current = current or Information()
        self.bestResult = best or Information()

    @property
    def id(self):
        """Get id."""
        return self._id if self._id else str(self)

    @id.setter
    def id(self, value):
        """Set id."""
        self._id = value
