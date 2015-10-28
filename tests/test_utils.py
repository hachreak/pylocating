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

"""Test utils."""

from __future__ import absolute_import, unicode_literals

from numpy import around, matrix, multiply, random
from pylocating.utils import _points_in_surface_sphere, \
    generate_points_in_surface_sphere, distance, \
    generate_points_random_in_surface_sphere, \
    generate_sequential_points


class TestUtils(object):

    """Test utils."""

    @staticmethod
    def _check_points(radius, points, center=None):
        """Check points."""
        square_radius = radius * radius
        center = center if center is not None else matrix([0, 0, 0])
        for point in points:
            point = point - center
            val = around(multiply(point, point).sum(), decimals=3)
            assert val == square_radius

    def test_point_in_surface_sphere(self):
        """Test point in surface sphere generation."""
        points = _points_in_surface_sphere(num_of_points=256)
        self._check_points(1, points)

    def test_point_in_surface_sphere_1(self):
        """Test point in surface sphere generation."""
        radius = 4
        points = generate_points_in_surface_sphere(
            center=matrix([0, 0, 0]), radius=radius, num_of_points=16)
        self._check_points(radius, points)

    def test_point_in_surface_sphere_2(self):
        """Test point in surface sphere generation."""
        center = matrix([5, 6, 7])
        radius = 1
        points = generate_points_in_surface_sphere(
            center=center, radius=radius, num_of_points=16)
        self._check_points(radius, points, center=center)

    def test_distance(self):
        """Test distance."""
        for i in range(20):
            point = matrix(random.random(3))
            assert 0 == distance(point, point)

        pa = matrix([5, 3, 4])
        pb = matrix([10, 3, 4])
        assert 5 == distance(pa, pb)

        pa = matrix([5, 3, 4])
        pb = matrix([5, 7, 4])
        assert 4 == distance(pa, pb)

        pa = matrix([5, 3, 4])
        pb = matrix([5, 3, 11])
        assert 7 == distance(pa, pb)

    def test_generate_points_random_in_surface_sphere_1(self):
        """Test generate points random in surface sphere."""
        center = matrix([0, 0, 0])
        radius = 1
        gen = generate_points_random_in_surface_sphere(center, radius)
        points = []
        for i in range(50):
            points.append(next(gen))
        self._check_points(radius, points, center)

    def test_generate_points_random_in_surface_sphere_2(self):
        """Test generate points random in surface sphere."""
        center = matrix([0, 0, 0])
        radius = 55
        gen = generate_points_random_in_surface_sphere(center, radius)
        points = []
        for i in range(50):
            points.append(next(gen))
        self._check_points(radius, points, center)

    def test_generate_points_random_in_surface_sphere_3(self):
        """Test generate points random in surface sphere."""
        center = matrix([45, -23, 67])
        radius = 1
        gen = generate_points_random_in_surface_sphere(center, radius)
        points = []
        for i in range(50):
            points.append(next(gen))
        self._check_points(radius, points, center)

    def test_generate_points_random_in_surface_sphere_4(self):
        """Test generate points random in surface sphere."""
        center = matrix([45, -23, 67])
        radius = 43
        gen = generate_points_random_in_surface_sphere(center, radius)
        points = []
        for i in range(50):
            points.append(next(gen))
        self._check_points(radius, points, center)

    def test_generate_sequential_points(self):
        """Test generate sequential points."""
        gen = generate_sequential_points(start_point=matrix([0, 0, 0]),
                                         random=random)

        point = next(gen)
        for i in range(30):
            next_point = next(gen)
            assert distance(point, next_point) < 0.87
            point = next_point
