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

from ..information import Information


class Particle(object):

    """Particle representation."""

    def __init__(self, environment, id=None,
                 current=None, best=None, velocity=None, vmax=None):
        """Init particle.

        :param environment: environment where the particle is inserted
        :param id: particle's id
        :param current: initialization of current position/fitness
        :param best: initialization of best position/fitness/velocity
        :param velocity: initialization if velocity
        :param vmax: maximun particle velocity
        """
        self._id = id
        self.environment = environment
        self.environment.register(self)
        self.vmax = vmax or 10
        self.velocity = velocity if velocity is not None else matrix([1, 1, 1])
        self._best = None
        self.current = current if current is not None else Information()

    @property
    def velocity(self):
        """Get velocity."""
        return self._velocity

    @velocity.setter
    def velocity(self, velocity):
        """Set (limited by vmax) velocity."""
        self._velocity = velocity
        # limit maximum velocity
        self._velocity[velocity > self.vmax] = self.vmax

    @property
    def current(self):
        """Get current information."""
        return self._current

    @current.setter
    def current(self, info):
        """Set current (set velocity<=vmax)."""
        # save new current value
        self._current = info
        # try to update also the best result
        self.best = info

    @property
    def best(self):
        """Get best Information."""
        return self._best

    @best.setter
    def best(self, info):
        """Set new best (only if it's better than the previous best value)."""
        if not self._best or info.fitness < self._best.fitness:
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
