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

from numpy import multiply

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
        # compute fitness
        difference = self.base - self.current.position
        square_difference = multiply(difference, difference)
        sum_square_diff = square_difference.sum(axis=1)
        result = (sum_square_diff - self.radius.transpose()).sum()
        # update best result
        self.best = Information(position=self.current.position,
                                fitness=result,
                                velocity=self.current.velocity)
        # return computed fitness value
        return result

    def move(self):
        """Compute next position and velocity of the particle.

        :return: new information of the particle
        """
        # information about the particle with best fitness
        binfo = self.environment.best.current
        w = self.environment.config['inertial_weight']
        c1 = self.environment.config['cognition']
        c2 = self.environment.config['social']
        # randomizer object that return random diagonal matrix
        # with values uniformed distributed in the interval [0,1)
        random = self.environment.config['random']
        # compute new position
        next_velocity = w * self.current.velocity + \
            c1 * random.random() * (binfo.velocity - self.current.velocity) + \
            c2 * random.random() * (binfo.position - self.current.position)
        next_position = self.current.position + next_velocity
        self.current = Information(position=next_position,
                                   velocity=next_velocity,
                                   fitness=self.current.fitness)
        return self.current
