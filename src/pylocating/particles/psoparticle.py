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

"""Particle Swarm Optimization Particle."""

from __future__ import absolute_import, unicode_literals

from numpy import multiply, absolute, matrix

from ..information import Information
from .particle import Particle


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


class PSOParticle(Particle):

    """PSO Particle."""

    def fitness(self):
        """Fitness function."""
        # prepare data
        base = self.environment.config['base']
        radius = self.environment.config['radius']
        (row, column) = base.shape
        position = matrix([self.current.position.A[0]]*row)
        tradius = radius.transpose()
        # compute fitness
        difference = base - position
        square_difference = multiply(difference, difference)
        sum_square_diff = square_difference.sum(axis=1)
        square_radius = multiply(tradius, tradius)
        result = absolute(sum_square_diff - square_radius).sum()
        # update current result
        self.current = Information(position=self.current.position,
                                   fitness=result)
        # return computed fitness value
        return result

    def move(self):
        """Compute next position and velocity of the particle.

        :return: new information of the particle
        """
        # global best position
        gbpos = self.environment.best.best.position
        # particle best position
        pbpos = self.best.position
        # particle current position and velocity
        pos = self.current.position
        vel = self.velocity
        # parameters
        w = self.environment.config['inertial_weight']
        c1 = self.environment.config['cognition']
        c2 = self.environment.config['social']
        # randomizer object that return random diagonal matrix
        # with values uniformed distributed in the interval [0,1)
        random = self.environment.config['random']
        # compute new position
        self.velocity = w * vel + \
            multiply(c1 * random.random(), (pbpos - pos)) + \
            multiply(c2 * random.random(), (gbpos - pos))
        next_position = pos + self.velocity
        # save
        self.current = Information(position=next_position,
                                   fitness=self.current.fitness)
        return self.current
