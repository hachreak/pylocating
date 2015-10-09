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

from numpy import matrix
from pylocating import Particle
from pylocating.environment import Environment, EmptyEnvironment
from pylocating.information import Information


class TestEnvironment(object):

    """Test environment."""

    def test_empty_environment(self):
        """Test empty environment."""
        env = Environment()
        with pytest.raises(EmptyEnvironment):
            env.best

    def test_env_best_result(self):
        """Test the computation of global best result."""
        env = Environment()
        position = matrix([0, 0, 0])

        particles = {}
        particles[1] = Particle(
            environment=env,
            best=Information(position=position, fitness=3))
        particles[2] = Particle(
            environment=env,
            best=Information(position=position, fitness=10))
        particles[3] = Particle(
            environment=env,
            best=Information(position=position, fitness=40))
        particles[4] = Particle(
            environment=env,
            best=Information(position=position, fitness=25))
        particles[5] = Particle(
            environment=env,
            best=Information(position=position, fitness=7))
        particles[6] = Particle(
            environment=env,
            best=Information(position=position, fitness=37))

        best = env.best
        assert particles[3] == best
        assert (particles[3].best == best.best).all()
