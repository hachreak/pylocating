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

"""Localization Environment."""

from __future__ import absolute_import, unicode_literals

import random

from numpy import matrix


__version__ = "0.1.0"


class EmptyEnvironment(Exception):

    """Empty Environment exception."""

    pass


class Environment(object):

    """It Contains all information shared by the particles."""

    def __init__(self, config):
        """Init environment.

        :param config: configuration:
              inertial_weight
              cognition
              social
              random (randomizer)
              base: position of M beacons (matrix: M x [X, Y, Z])
              radius: distance of the object computed by the M beacons (vector)
        """
        self.neighbors = [self]
        self.particles = {}
        self.config = config
        self.config['inertial_weight'] = self.config['inertial_weight'] \
            if 'inertial_weight' in self.config else 1
        self.config['cognition'] = self.config['cognition'] \
            if 'cognition' in self.config else 1
        self.config['social'] = self.config['social'] \
            if 'social' in self.config else 1
        self.config['random'] = self.config['random'] \
            if 'random' in self.config else random
        self.config['base'] = self.config['base'] \
            if 'base' in self.config else matrix([])
        self.config['radius'] = self.config['radius'] \
            if 'radius' in self.config else matrix([])

    def registerNeighbor(self, environment):
        """Register a environment."""
        if environment not in self.neighbors:
            self.neighbors.append(environment)
        if self not in environment.neighbors:
            environment.neighbors.append(self)

    def register(self, particle):
        """Register new particle."""
        self.particles[particle.id] = particle

    @property
    def neighborBest(self):
        """Find the global best looking inside all neighbor environments."""
        particles = [p.best for p in self.neighbors]
        return Environment._compute_best(particles)

    @property
    def best(self):
        """Compute realtime the new global best result."""
        return Environment._compute_best(self.particles.values())

    @staticmethod
    def _compute_best(particles):
        try:
            return min(particles, key=lambda v: v.best.fitness)
        except ValueError:
            raise EmptyEnvironment("""The environment is empty! """
                                   """Please insert new particles.""")
