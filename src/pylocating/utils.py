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

"""Utilities."""

from __future__ import absolute_import, unicode_literals

try:
    from functools import lru_cache
except ImportError:
    from functools32.functools32 import lru_cache

from numpy import matrix, linspace, meshgrid, sin, cos, pi, sqrt, multiply


@lru_cache(maxsize=100)
def _points_in_surface_sphere(num_of_points):
    """Return a point in the surface of the sphere.

    :param num_of_points: how many point to describe the surface
    :return: points
    """
    row = int(sqrt(num_of_points))
    [phi, theta] = meshgrid(linspace(0, 2 * pi, row), linspace(0, pi, row))
    phi = matrix(phi)
    theta = matrix(theta)
    x = multiply(sin(theta), cos(phi))
    y = multiply(sin(theta), sin(phi))
    z = cos(theta)

    return list(map(lambda x, y, z: matrix([x, y, z]), x.A1, y.A1, z.A1))


def generate_points_in_surface_sphere(center, radius, num_of_points):
    """Generate a point inside the surface of sphere.

    :param center: sphere center
    :param radius: sphere radius
    :param num_of_points: how many points to describe the surface
    :return: point as matrix
    """
    points = iter(_points_in_surface_sphere(num_of_points))
    while True:
        yield radius * next(points) + center


def distance(point_1, point_2):
    """Compute the euclidean distance from the two points."""
    return sqrt(sum((point_1-point_2).A[0]**2))
