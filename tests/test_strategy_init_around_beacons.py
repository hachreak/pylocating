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

"""Test Around Beacons Initialization Strategy."""

from __future__ import absolute_import, unicode_literals

from numpy import matrix
from pylocating.environment import Environment
from pylocating.strategies.init.position import around_beacons


class TestAroundBeaconsInitStrategy(object):

    """Test Around Beacons Initialization Strategy."""

    def test_generate(self):
        """Test generation."""
        class Random(object):

            """Randomizer."""

            def random(self):
                """Return random [0,1) matrix 3x1."""
                return matrix([1, 1, 1])

        env = Environment(
            config={
                'random': Random(),
            },
            base=matrix([
                [0, 0, 0],      # beacon 1
                [60, -40, 0],   # beacon 2
                [50, 50, 0],    # beacon 3
            ]),
        )
        num_beacons = len(env.base)
        position_gen = around_beacons(environment=env)

        for i in range(3*num_beacons):
            position = next(position_gen)
            new_val = env.base[i % num_beacons] + Random().random()
            assert (new_val == position).all()
