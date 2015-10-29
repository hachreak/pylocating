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

"""Moving point."""

from __future__ import absolute_import, unicode_literals

import logging

from numpy import matrix
from threading import Event, Thread
from time import sleep
from pylocating.utils import distance
from pylocating.benchmarks.utils import apply_noise_linear


class EnvironmentListener(object):

    """Connect Environment with MovingPointEngine and update radius."""

    def __init__(self, environment, error=1):
        """Init."""
        self.environment = environment
        self.error = error

    def position(self, point):
        """Update radius inside the environment."""
        disturbed_point_gen = apply_noise_linear(point=point, error=self.error)
        self.environment.radius = matrix(list(
            map(lambda b: distance(b, next(disturbed_point_gen)),
                self.environment.base)
        ))


class MovingPointEngine(Thread):

    """Animate a point: follow a defined path."""

    def __init__(self, config, listener, start_point, positions,
                 stop_condition=None):
        """Init moving particle.

        :param config: dict container for configuration
        :param point: point to move
        :param positions: next positions
        :param stop_condition: necessary condition to end the computation
        """
        super(MovingPointEngine, self).__init__()
        self.config = config
        self.shutdown_event = Event()
        self.listener = listener
        self.positions = positions
        self.point = start_point
        self.stop_condition = stop_condition or \
            (lambda mp: mp.iterations >= 100)
        self.logger = logging.getLogger(self.__class__.__module__ +
                                        "." + self.__class__.__name__)

    def run(self):
        """The main method for the thread.

        Called by the ``start()`` method.  Not to be called directly.
        """
        self.iterations = 0
        while not self.shutdown_event.is_set() and \
                not self.stop_condition(self):
            # generate next position
            self._move()

    def _move(self):
        """Move point."""
        try:
            self.point = next(self.positions)
            # alert listener
            self.listener.position(self.point)
            # sleep
            sleep(self.config['sleep'])
            # update counter
            self.iterations = self.iterations + 1
        except StopIteration:
            self.shutdown()

    def shutdown(self):
        """Shutdown the engine."""
        self.shutdown_event.set()


class LoggingMovingPointEngine(MovingPointEngine):

    """Add a logger."""

    def _move(self):
        # log nex position
        bestParticle = self.listener.environment.neighborBest
        self.logger.debug("{} {} {} {} {} {} {} {}".format(
            self.iterations,
            self.point.A[0][0],
            self.point.A[0][1],
            self.point.A[0][2],
            bestParticle.best.position.A[0][0],
            bestParticle.best.position.A[0][1],
            bestParticle.best.position.A[0][2],
            distance(self.point, bestParticle.best.position)
        ))
        super(LoggingMovingPointEngine, self)._move()
