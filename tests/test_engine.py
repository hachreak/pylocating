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

"""Test Python Localization Particle Engine."""

from __future__ import absolute_import, unicode_literals

from pylocating.engines.particle_engine import ParticleEngine


class TestParticleEngine(object):

    """Test particle engine."""

    def test_max_iterations(self):
        """Test max iterations."""
        class Particle(object):
            def fitness(self):
                pass

            def move(self):
                pass

        class Environment(object):
            def __init__(self):
                self.particles = [Particle() for i in range(4)]

        config = {}
        config["max_iterations"] = 100
        pe = ParticleEngine(config, Environment())
        pe.start()
        pe.join()

        assert pe.iterations == 100

        pe = ParticleEngine({}, Environment())
        pe.start()
        pe.join()

        assert pe.iterations == 20
