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

from pylocating.information import Information
from pylocating.engines.particle_engine import ParticleEngine


class TestParticleEngine(object):

    """Test particle engine."""

    def test_max_iterations(self):
        """Test max iterations."""
        class Particle(object):
            def __init__(self, id):
                self.id = id
                self.current = Information()
                self.velocity = 0
                self.best = self.current

            def fitness(self):
                pass

            def move(self):
                pass

        class Environment(object):
            def __init__(self):
                self.particles = {i: Particle(i) for i in range(4)}

        config = {}
        config["max_iterations"] = 100
        # without stop condition and max_iterations = 100
        pe = ParticleEngine(config=config, environment=Environment())
        pe.start()
        pe.join()

        assert pe.iterations == 100

        config = {}
        config["max_iterations"] = 100
        pe = ParticleEngine(config=config, environment=Environment(),
                            stop_condition=lambda x: False)
        pe.start()
        pe.join()

        assert pe.iterations == 100

        pe = ParticleEngine(config={}, environment=Environment(),
                            stop_condition=lambda x: False)
        pe.start()
        pe.join()

        assert pe.iterations == 20

        config = {}
        config["max_iterations"] = 100000
        pe = ParticleEngine(config=config, environment=Environment(),
                            stop_condition=lambda x: True)
        pe.start()
        pe.join()

        assert pe.iterations == 0
