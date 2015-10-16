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

"""Test Python Localization Environment."""

from __future__ import absolute_import, unicode_literals

import pytest
import random

from numpy import matrix
from pylocating.environment import Environment, EmptyEnvironment
from pylocating.information import Information
from pylocating.particles import Particle


class TestEnvironment(object):

    """Test environment."""

    def test_empty_environment(self):
        """Test empty environment."""
        env = Environment(config={})
        with pytest.raises(EmptyEnvironment):
            env.best

    def test_env_best_result(self):
        """Test the computation of global best result."""
        env = Environment(config={})
        position = matrix([0, 0, 0])

        particles = {}
        particles[1] = Particle(
            environment=env,
            current=Information(position=position, fitness=3))
        particles[2] = Particle(
            environment=env,
            current=Information(position=position, fitness=10))
        particles[3] = Particle(
            environment=env,
            current=Information(position=position, fitness=40))
        particles[4] = Particle(
            environment=env,
            current=Information(position=position, fitness=25))
        particles[5] = Particle(
            environment=env,
            current=Information(position=position, fitness=1))
        particles[6] = Particle(
            environment=env,
            current=Information(position=position, fitness=37))

        best = env.best
        assert particles[5] == best
        assert particles[5].best == best.best

    def test_randomizer(self):
        """Test randomizer."""
        class Random(object):
            def random(self):
                return "random"

        config = {}
        config['random'] = Random()
        env = Environment(config=config)

        assert env.config['random'].random() == "random"

        config['random'] = random
        env = Environment(config=config)

        assert 0 <= env.config['random'].random() < 1

    def test_cognition(self):
        """Test cognition."""
        config = {}
        config['cognition'] = 4
        env = Environment(config=config)

        assert env.config['cognition'] == 4

        env = Environment(config={})

        assert env.config['cognition'] == 1

    def test_social(self):
        """Test social."""
        config = {}
        config['social'] = 4
        env = Environment(config=config)

        assert env.config['social'] == 4

        env = Environment(config={})

        assert env.config['social'] == 1

    def test_inertial_weight(self):
        """Test inertial_weight."""
        config = {}
        config['inertial_weight'] = 4
        env = Environment(config=config)

        assert env.config['inertial_weight'] == 4

        env = Environment(config={})

        assert env.config['inertial_weight'] == 1

    def test_register_neighbord(self):
        """Test register neighboard."""
        env1 = Environment({})
        env2 = Environment({})

        assert env1 not in env2.neighbors
        assert env2 not in env1.neighbors
        assert len(list(filter(lambda x: x == env1, env1.neighbors))) == 1
        assert len(list(filter(lambda x: x == env2, env2.neighbors))) == 1

        env1.registerNeighbor(env2)

        assert env1 in env2.neighbors
        assert env2 in env1.neighbors
        assert len(list(filter(lambda x: x == env1, env1.neighbors))) == 1
        assert len(list(filter(lambda x: x == env2, env2.neighbors))) == 1

        # try to register 2 times
        env1.registerNeighbor(env2)

        assert len(list(filter(lambda x: x == env2, env1.neighbors))) == 1
        assert len(list(filter(lambda x: x == env1, env2.neighbors))) == 1

    def test_best_neighbor_env(self):
        """Test the best particle from all environments neighbor."""
        position = matrix([0, 0, 0])

        env1 = Environment({})
        env2 = Environment({})

        env1.registerNeighbor(env2)

        particles = {}
        particles[1] = Particle(
            environment=env1,
            current=Information(position=position, fitness=3))
        particles[2] = Particle(
            environment=env2,
            current=Information(position=position, fitness=10))
        particles[3] = Particle(
            environment=env1,
            current=Information(position=position, fitness=40))
        particles[4] = Particle(
            environment=env2,
            current=Information(position=position, fitness=25))
        particles[5] = Particle(
            environment=env1,
            current=Information(position=position, fitness=1))
        particles[6] = Particle(
            environment=env2,
            current=Information(position=position, fitness=37))

        best = env1.neighborBest
        assert particles[5] == best
        assert particles[5].best == best.best

        best = env2.neighborBest
        assert particles[5] == best
        assert particles[5].best == best.best
