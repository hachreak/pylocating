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

from ..utils import Randn3D
from .psoparticle import PSOParticle


class FollowBestParticle(PSOParticle):

    """Follow the best particle."""

    def __init__(self, *args, **kwargs):
        """Init randomizer."""
        self._random = Randn3D()
        super(FollowBestParticle, self).__init__(*args, **kwargs)

    def _move(self):
        """Move toward the best particle."""
        # global (in all environment) particle position
        gbpos = self.environment.neighborBest.best.position
        # parameters
        w = self.environment.config['inertial_weight']
        # compute new position
        return gbpos + w * self._random.random()
