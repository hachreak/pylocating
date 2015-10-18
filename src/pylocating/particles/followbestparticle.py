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

"""Particle Swarm Optimization Particle - follow the best results."""

from __future__ import absolute_import, unicode_literals

from numpy import multiply

from ..information import Information
from .psoparticle import PSOParticle


class FollowBestParticle(PSOParticle):

    """Follow the best particle."""

    def move(self):
        """Move toward the best particle."""
        # global (in all environment) particle position
        gbpos = self.environment.neighborBest.best.position
        # particle current position and velocity
        pos = self.current.position
        vel = self.velocity
        # parameters
        w = self.environment.config['inertial_weight']
        # randomizer object that return random diagonal matrix
        # with values uniformed distributed in the interval [0,1)
        random = self.environment.config['random']
        # compute new position
        self.velocity = multiply(w * random.random(), vel) + (gbpos - pos)
        next_position = pos + self.velocity
        # save
        self.current = Information(position=next_position,
                                   fitness=self.current.fitness)
        return self.current


class GlobalBestPSOParticle(PSOParticle):

    """PSO Particle conditioned by the global best particle.

    Not only in his environment, but the best from all environment.
    """

    def getBestParticle(self):
        """Return the best particle considering all environments."""
        return self.environment.neighborBest.best
