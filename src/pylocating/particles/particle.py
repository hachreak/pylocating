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

import logging
import threading

from numpy import matrix

from ..information import Information


class ParticleException(Exception):

    """Error in particle implementation."""


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
        self.logger = logging.getLogger(self.__class__.__module__ +
                                        "." + self.__class__.__name__)
        self._id = id
        self.environment = environment
        self.environment.register(self)
        self.vmax = vmax or 10
        self.velocity = velocity if velocity is not None else matrix([1, 1, 1])
        self._best = None
        self.current = current if current is not None else Information()
        self.lock = threading.RLock()

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
        self._velocity[velocity < -self.vmax] = -self.vmax

    @property
    def current(self):
        """Get current information."""
        return self._current

    @current.setter
    def current(self, info):
        """Set current and update best if necesary."""
        # save new current value
        self._current = info
        self.logger.debug(
            "[{}] fitness: {}\n".format(self.id, info.fitness))
        # Set new best (only if it's better than the previous best value).
        if not self._best or info.fitness < self._best.fitness:
            self.logger.debug(
                "[{}] best fitness: {}\n".format(self.id, info.fitness))
            self._best = info
            # update environment
            self.environment.best = self

    @property
    def best(self):
        """Get best Information."""
        return self._best

    @property
    def id(self):
        """Get id."""
        return self._id if self._id is not None else str(self)

    @id.setter
    def id(self, value):
        """Set id."""
        self._id = value

    def update_best_fitness(self):
        """Compute again the best fitness (because radius changed)."""
        with self.lock:
            self._best.fitness = self._fitness(self._best.position)

    def _fitness(self, position):
        """Compute the fitness and and return."""
        raise ParticleException("This function should be implemented.")

    def fitness(self):
        """Compute the fitness and update personal best."""
        fitness = self._fitness(self.current.position)
        self.current = Information(position=self.current.position,
                                   fitness=fitness)
        return fitness

    def _move(self):
        """Move the particle."""
        raise ParticleException("This function should be implemented.")

    def next(self):
        """Move and compute new fitness."""
        with self.lock:
            self.move()
            self.fitness()

    def move(self):
        """Move the particle."""
        next_position = self._move()
        self.current = Information(position=next_position,
                                   fitness=self.current.fitness)
        return next_position

    @property
    def index(self):
        """Get index number of the particle."""
        return list(self.environment.particles.keys()).index(self.id)
