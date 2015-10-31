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

"""Restart From the best position - Particle."""

from __future__ import absolute_import, unicode_literals

from copy import deepcopy

from .psoparticle import GlobalBestPSOParticle


class RestartFromBestParticle(GlobalBestPSOParticle):

    """PSOParticle: restart from best position if the environment change."""

    def __init__(self, *args, **kwargs):
        """Init."""
        super(RestartFromBestParticle, self).__init__(*args, **kwargs)

    def update_best_fitness(self):
        """Compute again the best fitness (because radius changed)."""
        super(RestartFromBestParticle, self).update_best_fitness()
        with self.lock:
            self.current = deepcopy(self.environment.best.best)
