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

"""Particle Engine."""

from __future__ import absolute_import, unicode_literals

from threading import Event, Thread


class ParticleEngine(Thread):

    """Abstract particle engine."""

    def __init__(self, config, environment):
        """Init particle engine.

        :param config: dict container for configuration
        :param environment: environment containing the particles
        """
        super(ParticleEngine, self).__init__()
        self.config = config
        self.shutdown_event = Event()
        self.environment = environment
        self.config['max_iterations'] = self.config['max_iterations'] \
            if 'max_iterations' in config else 20

    def run(self):
        """The main method for the thread.

        Called by the ``start()`` method.  Not to be called directly.
        """
        self.iterations = 0
        while not self.shutdown_event.is_set() and \
                self.config['max_iterations'] > self.iterations:
            # calculate fitness and update personal best
            for particle in self.environment.particles:
                particle.fitness()
            # move the particles
            for particle in self.environment.particles:
                particle.move()
            self.iterations = self.iterations + 1

    def shutdown(self):
        """Shutdown the engine."""
        self.shutdown_event.set()
