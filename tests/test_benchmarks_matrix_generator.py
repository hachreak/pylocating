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

"""Test Benchmarks Matrix generator."""

from __future__ import absolute_import, unicode_literals

from numpy import matrix
from pylocating.benchmarks.matrix_generator import \
    generate_matrix_of_points_in_cube


class TestBenchmarksMatrixGenerator(object):

    """Test Benchmarks Matrix generator."""

    def test_generate_matrix_of_points_in_cube(self):
        """Test generate matrix of points in cube."""
        num_of_points = 20
        side_length = 100
        gen = generate_matrix_of_points_in_cube(center=matrix([0, 0, 0]),
                                                side_length=side_length,
                                                num_of_points=num_of_points)
        for i in range(20):
            points = next(gen)
            assert (num_of_points, 3) == points.shape
            assert (points < (side_length / 2)).all()
            assert (points > (-side_length / 2)).all()
