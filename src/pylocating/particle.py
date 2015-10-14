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

"""Python Localization Particle."""

from __future__ import absolute_import, unicode_literals

from numpy import matrix
from .information import Information


class Particle(object):

    """Particle representation."""

    def __init__(self, base, radius, environment, id=None,
                 current=None, best=None, vmax=None):
        """Init particle.

        :param base: position of M beacons (matrix: M x [X, Y, Z])
        :param radius: distance of the object computed by the M beacons
            (vector)
        :param vmax: maximun particle velocity
        """
        self._id = id
        self.base = base
        self.environment = environment
        self.environment.register(self)
        self.vmax = vmax or 10
        self.current = current or Information()
        self._best = best or self.current
        self.radius = radius or matrix([0, 0, 0])

    @property
    def current(self):
        """Get current information."""
        return self._current

    @current.setter
    def current(self, info):
        """Set current (set velocity<=vmax)."""
        # set a maximum value for velocity
        info.velocity[info.velocity > self.vmax] = self.vmax
        # save new current value
        self._current = info

    @property
    def best(self):
        """Get best Information."""
        return self._best

    @best.setter
    def best(self, info):
        """Set new best (only if it's better than the previous best value)."""
        if info.fitness < self._best.fitness:
            self._best = info

    @property
    def id(self):
        """Get id."""
        return self._id if self._id else str(self)

    @id.setter
    def id(self, value):
        """Set id."""
        self._id = value

    def fitness(self):
        """Compute the fitness and update personal best."""
        pass

    def move(self):
        """Move the particle."""
        pass
