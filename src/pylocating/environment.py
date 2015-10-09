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

from numpy import matrix

from . import Information

__version__ = "0.1.0"


class EmptyEnvironment(Exception):

    """Empty Environment exception."""

    pass


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
            max = matrix(
                [p.best.fitness for p in self.particles.values()]).max()
            return list(
                filter((lambda p: p.best.fitness == max),
                       self.particles.values()))[0]
        except ValueError:
            raise EmptyEnvironment("""The environment is empty! """
                                   """Please insert new particles.""")
