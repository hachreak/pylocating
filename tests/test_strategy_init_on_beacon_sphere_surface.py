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

"""Test On Beacon Sphere Surface Initialization Strategy."""

from __future__ import absolute_import, unicode_literals

from numpy import matrix, around, multiply
from pylocating.environment import Environment
from pylocating.strategies.init.position import on_beacon_sphere_surface


class TestOnBeaconSphereSurfaceInitStrategy(object):

    """Test On Beacon Sphere Surface Initialization Strategy."""

    @staticmethod
    def _check_points(radius, points, center=None):
        """Check points."""
        square_radius = radius * radius
        center = center if center is not None else matrix([0, 0, 0])
        for point in points:
            point = point - center
            val = around(multiply(point, point).sum(), decimals=3)
            assert val == square_radius

    def test_generate(self):
        """Test generation."""
        env = Environment(
            config={},
            base=matrix([
                [0, 0, 0],      # beacon 1
                [60, -40, 0],   # beacon 2
                [50, 50, 0],    # beacon 3
            ]),
            radius=matrix([
                20,    # beacon 1
                60,    # beacon 2
                60,    # beacon 3
            ])
        )

        points = on_beacon_sphere_surface(environment=env, beacon_index=1,
                                          num_of_points=256)
        center = env.base[1]
        radius = env.radius.A[0][1]
        self._check_points(radius, points, center=center)
